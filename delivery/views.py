import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View, DetailView, detail
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.shortcuts import redirect

from delivery.models import Menu, MenuDetail, Restaurant, OrderTrans, OrderDetail, LocationUser
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
        context = {'menus': menus, 'path': path}
        return render(request, 'restaurant_detail.html', context)

class MyCart(View):

    def get(self, request):
        line_id = request.GET.get('user_id')
        user = CustomUser.objects.filter(line_id=line_id).first()
        ordertrans = OrderTrans.objects.filter(user=user, status=OrderTrans.INITIAL).order_by('-pk').first()
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
        context = {'result': tmp, 'total': total, 'ordertrans_id': ordertrans.id}
        return render(request, 'mycart.html', context)


class MenutDetail(View):

    def get(self, request, res_pk, pk):
        # line_id = request.GET.get('user_id', None)
        # user = CustomUser.objects.filter(line_id=line_id).first()
        # order = OrderTrans.objects.filter(user=user, restaurant__id=res_pk, status=OrderTrans.INITIAL).first()
        # detail = OrderDetail.objects.filter(order=order, menu__id=pk).first()
        menu = Menu.objects.filter(id=pk)
        menu = Menu.map_object_to_list(menu)
        context = {'menu': menu[0], 'detail': detail, 'restaurant_id': res_pk}
        return render(request, 'menu_detail.html', context)

class RestaurantView(View):

    def get(self, request):
        line_id = request.GET.get('user_id', None)
        branch_id = request.GET.get('branch_id', None)
        user = CustomUser.objects.filter(line_id=line_id).first()
        restaurants = Restaurant.objects.filter(branch_id=branch_id).order_by('show_id')
        if restaurants.count() > 2:
            restaurants = [ restaurants[0] , restaurants[1]]
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
            details = OrderDetail.objects.filter(order=order)
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
        restaurant_id = body['restaurant_id']
        with transaction.atomic():
            user = CustomUser.objects.filter(line_id=line_id).first()
            # restaurant = Restaurant.objects.filter(id=restaurant_id).first()
            ordertrans = OrderTrans.objects.filter(user=user, status=OrderTrans.INITIAL).order_by('-pk').first()
            if not ordertrans:  # make new order if lastest order status is not initial
                ordertrans = OrderTrans.objects.create(user=user)
            menu = Menu.objects.filter(id=menu_id).first()
            detail, created_detail = OrderDetail.objects.get_or_create(menu=menu, ordertrans=ordertrans)
            if action == 'add':
                detail.quantity += 1
            elif action == 'del':
                if detail.quantity > 0:
                    detail.quantity -= 1
                else:
                    detail.delete()
            detail.save(update_fields=['quantity'])
        return JsonResponse({})
    
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        line_id = body['line_id']
        user = CustomUser.objects.filter(line_id=line_id).first()
        try:
            OrderTrans.objects.filter(user=user, status=OrderTrans.INITIAL).update(status=OrderTrans.PROCESSING)
            return JsonResponse({'ok': True})
        except Exception as error:
            return JsonResponse({'ok': False, 'message': error})

    def delete(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        line_id = body['user_id']
        ordertrans_id = body['ordertrans_id']
        ordertrans = OrderTrans.objects.filter(id=ordertrans_id, status=OrderTrans.INITIAL).first()
        ordertrans.status = OrderTrans.FAILED
        ordertrans.save(update_fields=['status'])
        return JsonResponse({})
        