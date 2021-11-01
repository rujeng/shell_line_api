import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math

from django.core.paginator import Paginator
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.shortcuts import redirect
from django.core.exceptions import SuspiciousOperation

from otp.otp_service import Otp
from line.line_service import Line
from line.message import Message
from line.models import CarBrand, LineOfficial, LineLogin, LineMessage, CustomUser, Car , CarModel
from item.models import Item, TransactionForm
from line.form import WebForm
from utils.functions import get_paginator

# Create your views here.

def response_error_handler(request, exception=None):
    import pdb ; pdb.set_trace()
    return render(request, 'error.html')


class WebFormView(View):
    def get(self, request):
        return render(request, template_name='form.html')

    def post(self, request):
        line_id = request.GET.get("user_id", None)
        branch_id = request.GET.get("branch_id", None)
        full_name = request.POST.get('fullname', None)
        mobileno = request.POST.get('mobileno', None)
        meta_data = {'full_name': full_name, 'mobile': mobileno, 'line_id': line_id}
        return redirect(f'/otp/verify?user_id={line_id}&branch_id={branch_id}&full_name={full_name}&mobileno={mobileno}')


class LineHookView(View):

    def get(self, request):
        code = request.GET.get("code")
        branch_id = request.GET.get("branch_id")
        line_id, state = self.businesslogic(code, branch_id)
        user = CustomUser.objects.filter(line_id=line_id)
        if user:
            return redirect(f'/line/car/?user_id={line_id}&branch_id={branch_id}')
        if state:
            return redirect(f'/line/form?user_id={line_id}&branch_id={branch_id}')

        return render(request, 'error.html')

    def businesslogic(self, code, branch_id):
        # test
        '''
            return user object, boolean ถ้า state true ให้ redirect ไปที่ verify otp
            ถ้าเป็น false คือ ไม่มี user
        '''
        line = Line()
        line_login = LineLogin.objects.filter(line_official__id=branch_id , mode=1).first()
        channel_id = line_login.channel_id
        channel_secret = line_login.channel_secret
        get_token_response = line.get_token(
            code, branch_id, channel_id, channel_secret)
        print('get to ', get_token_response)
        if get_token_response['ok']:
            access_token = get_token_response['result']['access_token']
            get_profile_response = line.get_profile(access_token)
            if get_profile_response['ok']:
                user_id = get_profile_response['result']['userId']
                return user_id, True
        return None, False

class LineHistory(View):
    def get(self, request):
        code = request.GET.get("code")
        branch_id = request.GET.get("branch_id")
        line_id, state = self.businesslogic(code, branch_id)
        user = CustomUser.objects.filter(line_id=line_id)
        if user:
            return redirect(f'/line/history/?user_id={line_id}&branch_id={branch_id}&page=1&car_id=')
        if state:
            return redirect(f'/line/form?user_id={line_id}&branch_id={branch_id}')
        return render(request, 'error.html')

    def businesslogic(self, code,branch_id):
        line = Line()
        line_login = LineLogin.objects.filter(line_official__id=branch_id,mode=2).first()
        channel_id = line_login.channel_id
        channel_secret = line_login.channel_secret
        get_token_response = line.get_token_history(
            code,channel_id, channel_secret,branch_id)
        print('get to ', get_token_response)
        if get_token_response['ok']:
            access_token = get_token_response['result']['access_token']
            get_profile_response = line.get_profile(access_token)
            if get_profile_response['ok']:
                user_id = get_profile_response['result']['userId']
                return user_id, True
        return None, False


@method_decorator(csrf_exempt, name='dispatch')
class CreateCarAPIView(View):
    
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        line_id = body['line_id']
        model_id = body['model']
        car_register = body['car_register']
        model = CarModel.objects.filter(id=model_id).first()
        user = CustomUser.objects.filter(line_id=line_id).first()
        Car.objects.create(user_id=user, model=model, car_register=car_register)
        return JsonResponse({'ok': True})


@method_decorator(csrf_exempt, name='dispatch')
class MyCar(View):

    def get(self, request):
        line_id = request.GET.get('user_id', None)
        user = CustomUser.objects.filter(line_id=line_id).first()
        branch_id = request.GET.get('branch_id')
        official = []
        if branch_id == '1' or branch_id == '2':
            officiial_object = LineOfficial.objects.filter(Q(id=1) | Q(id=2))
            for i in officiial_object:
                official.append({
                    'name': i.name,
                    'id': i.id
                })
        car_objects = user.car_set.all()
        cars = Car.map_object_to_list(car_objects)
        list_brand = CarBrand.objects.filter(status=True)
        form_services = WebForm()
        context = {'cars': cars, 'cars_dropdown': list_brand, 'form_services': form_services,'official': official}
        return render(request, 'add_car.html', context=context)

    def post(self, request):
        line_id = request.GET.get('user_id')
        branch_id = int(request.GET.get('branch_id'))
        if branch_id == 1:
             branch_id = request.POST.get("branch_id", None)
        form = WebForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.filter(line_id=line_id).first()
            car_id = request.POST['car_id']
            date = request.POST['date']
            time = request.POST['time']
            message = Message()
            service_detail = message.makeservice_detail(request)
            branch_name = LineOfficial.objects.filter(id=branch_id).first()
            car = Car.objects.filter(id=car_id).first()
            meta_dat = {'fullname' : user.full_name,'mobileno': user.mobile_no, 'car_id': car_id,
                         'model' : car.model, 'line_id': line_id,'branch_id': branch_id,'branch_name' : branch_name,
                        'date': date,'time': time ,'service_detail' : service_detail}
            if self.businesslogic(meta_dat):
                  return render(request, 'success.html')
            return render(request, 'error.html')

    def businesslogic(self, meta_dat):
            car_id = meta_dat["car_id"]
            mobileno = meta_dat["mobileno"]
            branch_id = meta_dat["branch_id"]
            line_id = meta_dat["line_id"]
            service_detail = meta_dat["service_detail"]
            date = meta_dat["date"]
            time = meta_dat["time"]
            date_time_str = f'{date} {time}'
            appointed_date = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
            car = Car.objects.filter(id=car_id).first()
            line = Line()
            line_message = LineMessage.objects.filter(id=branch_id).first()
            channel_access_token = line_message.channel_access_token
            message = Message()
            message_data_push_noti,message_data_notify = message.makemessage(meta_dat,car)
            res = line.push_message(
                meta_dat, channel_access_token,message_data_push_noti)
            if res['ok']:
                line.notify(message_data_notify, settings.ACCESS_TOKEN)
                user = CustomUser.objects.filter(line_id=line_id).first()
                TransactionForm.objects.create(car=car, user=user, appointed_date=appointed_date, 
                                         description=service_detail, branch_id=int(branch_id))
                return True
            return False


class CarSeries(View):

    def get(self, request):
        seriesId = request.GET.get('seriesId', None)
        series = CarModel.objects.filter(brand__id=seriesId, status=True)
        car_series = CarModel.map_object_to_json(series)
        return JsonResponse({'series': car_series})


class MyHistory(View):

    show_list = 2

    def get_transaction_detail(self, transaction):
        total_price = 0
        result = []
        tran_details = transaction.sale_detail.all()
        for detail in tran_details:
            total_price += detail.quantity * detail.item.sell_price
            result.append({
                'item': detail.item.name,
                'quantity': detail.quantity,
                'price': detail.sell_price,
            })
        return result, total_price
            

    def get_first_transaction_by_car(self, line_id):
        user = CustomUser.objects.filter(line_id=line_id).first()
        cars = Car.objects.filter(user_id=user)
        result = []
        for car in cars:
            tran = TransactionForm.objects.filter(user=user, car=car).order_by('-created_at').first()
            details, total_price = self.get_transaction_detail(transaction=tran)
            branch = LineOfficial.objects.filter(id=tran.branch_id).first()
            transaction_by_car = {
                'details': details,
                'branch': branch.name if branch else 'None',
                'car_register': tran.car.car_register,
                'brand': tran.car.model.brand.name,
                'created_at': self.__get_day(tran.created_at),
                'created_date': datetime.strftime(tran.created_at, '%d/%m/%Y'),
                'appointed_date': tran.appointed_date,
                'status': tran.status,
                'total_price': total_price,
                'next_service': self.__next_service(tran.created_at)
            }
            result.append(transaction_by_car)
        return result, cars
        
    def get(self, request):
        page = request.GET.get('page', 1)
        car_id = request.GET.get('car_id', None)
        line_id = request.GET.get('user_id', None)
        car = []
        if not line_id:
            return render(request, 'error.html')
        user = CustomUser.objects.filter(line_id=line_id).first()
        if car_id:
            car = Car.get_car_by_id(car_id).first()
            trans = TransactionForm.objects.filter(user=user, car=car).order_by('-created_at')
        else:
            trans = TransactionForm.objects.filter(user=user).order_by('-created_at')
        cars = Car.objects.filter(user_id=user)
        paginator = get_paginator(trans, self.show_list, page)
        start_page = self.show_list * (int(page)-1)
        end_page = start_page + self.show_list
        result = self.get_slice_transaction(trans, start_page, end_page)
        context = {'result': result, 'fullname': user.full_name, 'mobile': user.mobile_no, 
        'page_obj': paginator['page_obj'], 'cars_dropdown': cars, 'car': car,
        'next_page': paginator['next_page'], 'prv_page': paginator['prv_page']
        }
        return render(request, 'transaction-list.html', context=context)

    def get_transaction_by_car(self, car_id, user):
        car = []
        if car_id:
            car = Car.objects.filter(id=int(car_id)).first()
            transactions = TransactionForm.objects.filter(user_id=user, car=car)
            car = Car.map_object_to_list([car])
        else:
            transactions = TransactionForm.objects.filter(user_id=user)
        return transactions.filter(status=TransactionForm.DONE), car

    def get_slice_transaction(self, transactions, start_page, end_page):
        result = []
        for tran in transactions[start_page:end_page]:
            details = []
            total_price = 0
            tran_details = tran.sale_detail.all()
            for detail in tran_details:
                total_price += detail.quantity * detail.item.sell_price
                details.append({
                    'item': detail.item.name,
                    'quantity': detail.quantity,
                    'price': detail.sell_price,
                })
            car_register = tran.car.car_register
            branch = LineOfficial.objects.filter(id = tran.branch_id).first()
            transaction_by_car = {
                'details': details,
                'branch': branch.name if branch else 'None',
                'car_register': tran.car.car_register,
                'brand': tran.car.model.brand.name,
                'model': tran.car.model.name,
                'created_at': self.__get_day(tran.created_at),
                'created_date': datetime.strftime(tran.created_at, '%d/%m/%Y'),
                'appointed_date': tran.appointed_date,
                'status': tran.status,
                'total_price': total_price,
                'next_service': self.__next_service(tran.created_at)
            }
            result.append(transaction_by_car)
            # group transaction by car
            # if result.get(car_register):
            #     result[car_register]['data'].append(transaction_by_car)
            # else:
            #     result.update({car_register: {'car_register': tran.car.car_register,'brand':tran.car.brand,'model':tran.car.model, 'data': [transaction_by_car]}})
        return result

    def __get_day(self, datetime):
        diff = timezone.now() - datetime
        day = diff.days
        if day <= 0:
            return 'วันนี้'
        return f'{day} วันที่แล้ว'

    def __next_service(self, datetime):
        next_service = datetime + relativedelta(months=4)
        return next_service.strftime('%d/%m/%Y')



class ListItem(View):

    show_list = 10

    def pageination(self, obj, current_page):
        pages = math.ceil(len(obj)/self.show_list)
        pages = [{'page': i} for i in range(1, pages+1)]
        prev_p = False
        next_p = False
        return pages

    def get(self,request):
        search_name = ''
        page = request.GET.get('page', 1)
        search_name = request.GET.get('search_name', '')
        start_page = self.show_list * (int(page)-1)
        end_page = start_page + self.show_list
        result = []
        items = Item.objects.filter(name__icontains=search_name)
        for i in items[start_page:end_page]:
            result.append({
                'name': i.name,
                'sell_price': i.sell_price
            })
        paginator = Paginator(items, self.show_list)
        page_obj = paginator.get_page(page)
        path = 'search_name='+search_name
        context = {'result' : result,'page_obj': page_obj, 'path': path}
        return render(request, 'item-list.html', context=context)

# import requests
@method_decorator(csrf_exempt, name='dispatch')
class Testview(View):

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        reply_token = body['events'][0]['replyToken']

        return JsonResponse({},status=200)

    def get(self, request):
        import pdb ; pdb.set_trace()
        url='https://api.line.me/v2/bot/message/reply'
        data = {
            "replyToken":"nHuyWiB7yP5Zw52FIkcQobQuGDXCTA",
            "messages":[
                {
                    "type":"text",
                    "text":"Hello, user"
                },
                {
                    "type":"text",
                    "text":"May I help you?"
                }
            ]
        }
        res = requests.post(url, data=data)
        # contact_list = TransactionForm.objects.all()
        # page_number = int(request.GET.get('page', 1))
        # paginator = Paginator(contact_list, 5) # Show 25 contacts per page.

        # page_obj = paginator.get_page(page_number)
        # prv = page_obj.previous_page_number
        # next_page = page_obj.next_page_number
        # if page_number <= 1:
        #     prv = 1
        # if page_number >= paginator.count:
        #     next_page = paginator.count
        
        # context = {'page_obj': page_obj, 'prv': prv, 'next': next_page}

        return render(request, 'otp.html', context=context)
    
    # def post(self, request):
    #     form = WebForm(request.POST)
    #     print('---------', form.is_valid())
    #     if form.is_valid():

    #         print(form.cleaned_data)
    #     print(form.errors)
    #     return render(request, 'list.html', context={'form': form})
    #     if form.is_valid():
    #         return

