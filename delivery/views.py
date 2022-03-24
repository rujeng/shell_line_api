import json
import requests

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View, DetailView, detail
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from delivery.models import Menu, Restaurant, Order, OrderDetail
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
        orders = Order.objects.filter(user=user, status=Order.INITIAL)
        result = []
        total = 0
        for order in orders:
            details = order.order_detail.all()
            details_result = []
            for detail in details:
                details_result.append({
                    'name': detail.menu,
                    'price': detail.price,
                    'quantity': detail.quantity
                })
                total += detail.price * detail.quantity
            result.append({
                'restaurant': order.restaurant.name,
                'details': details_result,
            })
        context = {'result': result, 'total': total}
        return render(request, 'mycart.html', context)


class MenutDetail(View):

    def get(self, request, res_pk, pk):
        line_id = request.GET.get('user_id', None)
        user = CustomUser.objects.filter(line_id=line_id).first()
        order = Order.objects.filter(user=user, restaurant__id=res_pk, status=Order.INITIAL).first()
        detail = OrderDetail.objects.filter(order=order, menu__id=pk).first()
        menu = Menu.objects.filter(id=pk)
        menu = Menu.map_object_to_list(menu)
        context = {'menu': menu[0], 'detail': detail}
        return render(request, 'menu_detail.html', context)

class RestaurantView(View):

    def get(self, request):
        restaurants = Restaurant.objects.all()
        context = {'restaurants': restaurants}
        return render(request, 'restaurant.html', context=context)

        
class OrderView(View):
    
    def get(self, request):
        orders = Order.objects.all().order_by('-pk')
        object_list = Order.map_object_to_list(orders)
        context = {'object_list': object_list}
        return render(request, 'order.html', context)
    
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
        orders = Order.objects.filter(user=user, status=Order.INITIAL)
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
            restaurant = Restaurant.objects.filter(id=restaurant_id).first()
            order = Order.objects.filter(user=user, status=Order.INITIAL).order_by('-pk').first()
            if not order:  # make new order if lastest order status is not initial
                order = Order.objects.create(user=user, restaurant=restaurant)
            menu = Menu.objects.filter(id=menu_id).first()
            detail, created_detail = OrderDetail.objects.get_or_create(menu=menu, order=order)
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
            Order.objects.filter(user=user, status=Order.INITIAL).update(status=Order.PROCESSING)
            return JsonResponse({'ok': True})
        except Exception as error:
            return JsonResponse({'ok': False, 'message': error})

        