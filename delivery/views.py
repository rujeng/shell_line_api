from datetime import datetime
import json
from math import fabs

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View, DetailView, detail
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.shortcuts import redirect
from line.line_service import Line
from line.models import LineMessage , LineOfficial
from delivery.line_message import line_message

from delivery.models import Menu, MenuDetail, Restaurant, OrderTrans, OrderDetail, LocationUser, ConfigDetail
from line.models import CustomUser

@method_decorator(csrf_exempt, name='dispatch')
class WebhookAPI(View):

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        reply_token = body['events'][0]['replyToken']
        
        return JsonResponse({},status=200)


class RestaurantDetail(View):

    def get(self, request, pk):
        menus = Menu.objects.filter(restaurant__id=pk)
        menus = Menu.map_object_to_list(menus)
        path = request.path
        restaurant = Restaurant.objects.filter(id=pk).first()
        print(restaurant.avatar.url)
        context = {'menus': menus, 'path': path, 'restaurant': restaurant}
        return render(request, 'restaurant_detail.html', context)

class MyCart(View):

    def get(self, request):
        line_id = request.GET.get('user_id')
        user = CustomUser.objects.filter(line_id=line_id).first()
        ordertrans = OrderTrans.objects.filter(user=user, status=OrderTrans.INITIAL).order_by('-pk').first()
        if not ordertrans:
            return render(request, 'mycart.html')
        order_detail_list = OrderDetail.objects.filter(ordertrans=ordertrans)
        result_dict = dict()
        total = 0
        for order in order_detail_list:
            restaurant_name = order.menu.restaurant.name
            menu_detail_id_list = order.menu_detail_id
            details = []
            if menu_detail_id_list:
                menu_detail_obj = MenuDetail.objects.filter(id__in=menu_detail_id_list.split(','))
                for item in menu_detail_obj:
                    details.append({
                        'name': item.detail,
                        'on_top_price': item.on_top_price,
                    })
                    total += item.on_top_price
                details = MenuDetail.map_to_list(menu_detail_obj)
            detail_dict = {'menu': order.menu.name, 'price': order.menu.price, 'quantity': order.quantity, 'details': details, 'description': order.description}
            total += order.quantity * order.menu.price
            if restaurant_name in result_dict:
                result_dict[restaurant_name].append(detail_dict)
            else:
                result_dict[restaurant_name] = [detail_dict]
        tmp = []
        for key, val in result_dict.items():
            tmp.append({'name': key, 'detail_list': val})
        locations_user = LocationUser.objects.filter(user=user)
        context = {'result': tmp, 'total': total, 'ordertrans_id': ordertrans.id, 'locations_user': locations_user}
        # print(context)
        return render(request, 'mycart.html', context)



class NewMyCart(View):

    def get(self, request):
        line_id = request.GET.get('user_id')
        user = CustomUser.objects.filter(line_id=line_id).first()
        ordertrans = OrderTrans.objects.filter(user=user, status=OrderTrans.INITIAL).order_by('-pk').first()
        if not ordertrans:
            return render(request, 'cart1.html')
        order_detail_list = OrderDetail.objects.filter(ordertrans=ordertrans).order_by('menu__restaurant_id')
        result_dict = {}
        all_price = 0
        for order_detail in order_detail_list:
            menu_detail_id_list = order_detail.menu_detail_id
            details = []
            total_on_top_price = 0
            total_price = 0
            if menu_detail_id_list:
                menu_detail_obj = MenuDetail.objects.filter(id__in=menu_detail_id_list.split(','))
                for item in menu_detail_obj:
                    details.append({
                        'name': item.detail,
                        'on_top_price': item.on_top_price,
                    })
                    total_on_top_price += item.on_top_price
            price = order_detail.menu.price * order_detail.quantity
            total_price += price + total_on_top_price
            all_price += total_price
            temp = {'name': order_detail.menu.name, 'quantity': order_detail.quantity, 'price': price, 'details': details, 
                    'total_price_by_menu': total_price, 'description': order_detail.description}
            restaurant_name = order_detail.menu.restaurant.name
            if restaurant_name in result_dict:
                result_dict[restaurant_name].append(temp)
            else:
                result_dict[restaurant_name] = [temp]
        tmp = []
        for key, val in result_dict.items():
            tmp.append({'name': key, 'detail_list': val})
        for i in tmp:
            total_price_by_restaurant = 0
            for menu in i['detail_list']:
                total_price_by_restaurant += menu['total_price_by_menu']
            i['total_price_by_restaurant'] = total_price_by_restaurant
        context = {'result': tmp, 'total': all_price, 'ordertrans_id': ordertrans.id, 'locations_user': ''}
        return render(request, 'cart1.html', context=context)


class MenutDetail(View):

    def get(self, request, res_pk, pk):
        # line_id = request.GET.get('user_id', None)
        # user = CustomUser.objects.filter(line_id=line_id).first()
        # order = OrderTrans.objects.filter(user=user, restaurant__id=res_pk, status=OrderTrans.INITIAL).first()
        # detail = OrderDetail.objects.filter(order=order, menu__id=pk).first()
        menu = Menu.objects.filter(id=pk)
        menu = Menu.map_object_to_list(menu)
        restaurant = Restaurant.objects.filter(id=res_pk).first()
        context = {'menu': menu[0], 'detail': detail, 'restaurant': restaurant}
        return render(request, 'menu_detail.html', context)

class RestaurantView(View):

    def get(self, request):
        line_id = request.GET.get('user_id', None)
        branch_id = request.GET.get('branch_id', None)
        user = CustomUser.objects.filter(line_id=line_id).first()
        restaurants = Restaurant.objects.filter(branch_id=branch_id).order_by('show_id')
        # if restaurants.count() > 2:
        #     restaurants = [ restaurants[0] , restaurants[1]]
        context = {'restaurants': restaurants, 'full_name': user.full_name,'phone':user.mobile_no}
        return render(request, 'restaurant.html', context=context)

class RestaurantAllView(View):

    def get(self, request):
        branch_id = request.GET.get('branch_id', None)
        restaurants = Restaurant.objects.filter(branch_id=branch_id).order_by('show_id')
        context = {'restaurants': restaurants}
        return render(request, 'restaurant_all.html', context=context)

class OrderView(View):
    
    def get(self, request):
        orders = OrderTrans.objects.all().order_by('-pk')
        object_list = OrderTrans.map_object_to_list(orders)
        context = {'object_list': object_list}
        return render(request, 'order.html', context)

class Enroll(View):
        def get(self, request):
            return render(request, 'Enroll.html')

class LocationDetail(View):
        def get(self, request):
            line_id = request.GET.get("user_id", None)
            user = CustomUser.objects.filter(line_id=line_id).first()
            history = LocationUser.objects.filter(user=user)
            context = {'historys': history}
            return render(request, 'location_detail.html', context=context)    

class LocationSave(View):
        def get(self, request):
            return render(request, 'location_save.html')
        
        def post(self, request):
            line_id = request.GET.get("user_id", None)
            branch_id = request.GET.get("branch_id", None)
            locationName = request.POST.get('locationName', None)
            latitude = request.POST.get('latitude', None)
            longitude = request.POST.get('longitude', None)
            detail_1st = request.POST.get("detail1st",None)
            detail_2nd = request.POST.get("detail2nd",None)
            user = CustomUser.objects.filter(line_id=line_id).first()
            LocationUser.objects.create(name=locationName, user=user, latitude=float(latitude), 
                                         longtitude=float(longitude), detail_1st=detail_1st, detail_2nd=detail_2nd)
            return redirect(f'/delivery/location_detail?user_id={line_id}&branch_id={branch_id}')

class History(View):
     def get(self,request,pk):
        line_id = request.GET.get('user_id', None)
        user = CustomUser.objects.filter(line_id=line_id).first()
        ordertrans = OrderTrans.objects.filter(user=user,id=pk)
        if not ordertrans:
            return render(request, 'failed.html')
        order_detail_list = OrderDetail.objects.filter(ordertrans=ordertrans[0])
        result_dict = dict()
        total = 0
        for order in order_detail_list:
            restaurant_name = order.menu.restaurant.name
            menu_detail_id_list = order.menu_detail_id
            details = []
            if menu_detail_id_list:
                menu_detail_obj = MenuDetail.objects.filter(id__in=menu_detail_id_list.split(','))
                for item in menu_detail_obj:
                    details.append({
                        'name': item.detail,
                        'on_top_price': item.on_top_price,
                    })
                    total += item.on_top_price
                details = MenuDetail.map_to_list(menu_detail_obj)
            detail_dict = {'menu': order.menu.name, 'price': order.menu.price, 'quantity': order.quantity, 'details': details, 'description': order.description}
            total += order.quantity * order.menu.price
            if restaurant_name in result_dict:
                result_dict[restaurant_name].append(detail_dict)
            else:
                result_dict[restaurant_name] = [detail_dict]
        tmp = []
        for key, val in result_dict.items():
            tmp.append({'name': key, 'detail_list': val})
        context = {'result': tmp, 'total': total,'ordertrans':ordertrans[0],'payment_method':self.mapping_payment_method(ordertrans[0].payment_method)}
        return render(request, 'order_history.html',context=context)
        

class TestMap(View):
        def get(self, request):
            return render(request, 'testmap.html')

@method_decorator(csrf_exempt, name='dispatch')
class OrderAPI(View):

    #notify
    def get(self, request):
        # ถ้าไม่มี user ในระบบทำยังไง
        line_id = request.GET.get('user_id', None)
        user = CustomUser.objects.filter(line_id=line_id).first()
        orders = OrderTrans.objects.filter(user=user, status=OrderTrans.INITIAL)
        # get number of items in order's user
        count = 0
        for order in orders:
            details = OrderDetail.objects.filter(ordertrans=order)
            for detail in details:
                count += detail.quantity
        return JsonResponse({'count': count})

    def get_order_detail_quantity(self, details):
        count = 0
        for detail in details:
            count += detail.quantity
        return count

    def patch(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        menu_id = body['menu_id']
        action = body['action']
        line_id = body['user_id']
        quantity = body['quantity']
        description = body['description']
        restaurant_id = body['restaurant_id']
        with transaction.atomic():
            user = CustomUser.objects.filter(line_id=line_id).first()
            # restaurant = Restaurant.objects.filter(id=restaurant_id).first()
            ordertrans = OrderTrans.objects.filter(user=user, status=OrderTrans.INITIAL).order_by('-pk').first()
            if not ordertrans:  # make new order if lastest order status is not initial
                ordertrans = OrderTrans.objects.create(user=user)
            menu = Menu.objects.filter(id=menu_id).first()
            if action == 'add':
                detail = OrderDetail.objects.create(menu=menu, ordertrans=ordertrans, quantity=quantity, description=description)
            # if action == 'add':
            #     detail.quantity += 1
            # elif action == 'del':
            #     if detail.quantity > 0:
            #         detail.quantity -= 1
            #     else:
            #         detail.delete()
            # detail.save(update_fields=['quantity'])
        return JsonResponse({})
    
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        line_id = body['line_id']
        branch_id = body['branch_id']
        location_id = body['location_id']
        payment_method_id = body['payment_method_id']
        user = CustomUser.objects.filter(line_id=line_id).first()
        try:
            #ordertrans = OrderTrans.objects.filter(user=user, status=OrderTrans.INITIAL).update(status=OrderTrans.PROCESSING)
            ordertrans = OrderTrans.objects.filter(user=user, status=OrderTrans.INITIAL).first()
            line = Line()
            branch_name = LineOfficial.objects.filter(id=branch_id).first()
            lineMessage = LineMessage.objects.filter(id=branch_id).first()
            channel_access_token = lineMessage.channel_access_token
            message = line_message()
            meta_dat = {'line_id':line_id,'branch_name':branch_name}
            message_data_push_noti = message.order_message(meta_dat=meta_dat,tran=ordertrans)
            res = line.push_message(
                    meta_dat, channel_access_token,message_data_push_noti)
            if res['ok']:
                location_user = LocationUser.objects.filter(id=location_id).first()
                ordertrans.status = OrderTrans.PROCESSING
                ordertrans.location_user = location_user
                ordertrans.payment_method = payment_method_id
                ordertrans.updated_at = datetime.now()
                ordertrans.branch_id = branch_id
                ordertrans.save()
            #   line.notify(message_data_notify, settings.ACCESS_TOKEN)
            return JsonResponse({'ok': True})
        except Exception as error:
            print(error)
            return JsonResponse({'ok': False, 'message': error})
        
    def checkOpeningTime():
        is_open = False
        now = datetime.now()
        open_time_str = ConfigDetail.objects.filter(name='Open_Time').first()
        close_time_str = ConfigDetail.objects.filter(name='Close_Time').first()
        open_time = datetime.strptime(open_time_str, '%H:%M:%S')
        close_time = datetime.strptime(close_time_str, '%H:%M:%S')
        current_time = now.strftime("%H:%M:%S")
        if current_time >= open_time and current_time <= close_time:
            is_open = True
        return is_open

    def delete(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        line_id = body['user_id']
        ordertrans_id = body['ordertrans_id']
        ordertrans = OrderTrans.objects.filter(id=ordertrans_id, status=OrderTrans.INITIAL).first()
        ordertrans.status = OrderTrans.FAILED
        ordertrans.save(update_fields=['status'])
        return JsonResponse({})
        