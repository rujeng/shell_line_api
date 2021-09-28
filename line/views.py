import json

from django.conf import settings
from django.core.checks.messages import Debug
from django.utils import timezone
from line import message
from line.line_service import Line
from line.message import Message
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from line.models import LineOfficial, TransactionForm, LineLogin, LineMessage, CustomeUser, Car
# from line.form.web_form import WebForm
from django.shortcuts import redirect
from django.core.exceptions import SuspiciousOperation
# Create your views here.


class WebForm(View):
    def get(self, request):
        line_id = request.GET.get('user_id')
        user, is_existed = CustomeUser.objects.get_or_create(line_id=line_id)
        cars = []
        cars_object = Car.objects.filter(user_id=user)
        for car in cars_object:
            cars.append({
                'brand': car.brand,
                'model': car.model,
                'car_register': car.car_register,
                'id': car.id
            })
        form_services = ServiceForm()
        context = {'user': user, 'cars_dropdown': Car.CARS, 'cars': cars, 'form_services': form_services}
        return render(request, template_name='form.html', context=context)

    def post(self, request):
        line_id = request.GET.get("user_id", 'test')
        branch_id = request.GET.get("branch_id", None)
        fullname = request.POST.get('fullname', None)
        mobileno = request.POST.get('mobileno', None)
        car_id = request.POST.get('car_id', None)
        date = request.POST.get('date', None)
        time = request.POST.get('time', None)
        firstname = fullname.split(' ')[0]
        lastname = fullname.split(' ')[-1]
        fullname = f'{firstname} {lastname}'
        message = Message()
        service_detail = message.makeservice_detail(request)
        car = Car.objects.filter(id=car_id).first()
        meta_dat = {'firstname': firstname, 'lastname': lastname,'fullname' : fullname,
                    'mobileno': mobileno, 'car_id': car_id, 'brand': car.brand,
                    'model':car.model,'line_id': line_id, 'branch_id': branch_id, 
                    'date': date,'time': time ,'service_detail' : service_detail }
        print(meta_dat)

        return render(request, 'success.html')
        # if self.__businesslogic(meta_dat):
        #      return render(request, 'success.html')
        # return render(request, 'error.html')

    def __businesslogic(self, meta_dat):
        mobileno = meta_dat["mobileno"]
        branch_id = meta_dat["branch_id"]
        line_id = meta_dat["line_id"]
        branch_name = LineOfficial.objects.filter(id=branch_id).first()
        line = Line()
        line_message = LineMessage.objects.filter(branch_id=branch_id).first()
        channel_access_token = line_message.channel_access_token
        message = Message()
        message_data_push_noti,message_data_notify = message.makemessage(meta_dat)
        res = line.push_message(
            meta_dat, channel_access_token,message_data_push_noti)
        if res['ok']:
            #message = json.dumps(meta_dat, ensure_ascii=False)
            line.notify(message_data_notify, settings.ACCESS_TOKEN)
            user, is_existed = CustomeUser.objects.get_or_create(line_id=line_id)
            user.first_name = meta_dat['firstname']
            user.last_name = meta_dat['lastname']
            user.mobile_no = mobileno
            user.save()
            TransactionForm.objects.create(user_id=user, car_id=int(
                meta_dat['car_id']), appointed_date=timezone.now(), branch_id=1)
            # TransactionForm.objects.create(meta_data = meta_dat,line_message = line_message,user_id = user_id)
            return True
        return False


class LineHookView(View):

    def get(self, request):
        code = request.GET.get("code")
        branch_id = request.GET.get("branch_id")
        line_id, state = self.__businesslogic(code, branch_id)
        if state:
            return redirect(f'/line/form?user_id={line_id}&branch_id={branch_id}')

        return render(request, 'error.html')

        # line = Line()
        # queries = { 'code' : code , 'channel_id' : channel_id }
        # get_token_response = line.get_token(queries)

    def __businesslogic(self, code, branch_id):
        line = Line()
        line_login = LineLogin.objects.filter(branch_id=branch_id).first()
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


@method_decorator(csrf_exempt, name='dispatch')
class MyCar(View):

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        line_id = body['line_id']
        brand = body['brand']
        model = body['model']
        car_register = body['car_register']
        user = CustomeUser.objects.filter(line_id=line_id).first()
        Car.objects.create(user_id=user, brand=brand,
                           model=model, car_register=car_register)
        return JsonResponse({'ok': True})

from line.form import NameForm, ServiceForm, GeeksForm
class Testview(View):
    
    def get(self, request):
        form = GeeksForm()
        return render(request, 'list.html', context={'form': form})
        

    def post(self, request):
        form = ServiceForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
        return render(request, 'list.html', context={'form': form})
        if form.is_valid():
            return