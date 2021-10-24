import json
import requests

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
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


class RestaurantView(View):

    def get(self, request):
        # restaurants in branch = 1
        restaurants = Restaurant.objects.all()
        object_list = Restaurant.get_menu_list(restaurants)
        context = {'object_list': object_list}
        return render(request, 'restaurant.html', context=context)

        
class OrderView(View):
    
    def get(self, request):
        return render(request, 'order.html')
    

@method_decorator(csrf_exempt, name='dispatch')
class OrderAPI(View):

    def get(self, request):
        # ถ้าไม่มี user ในระบบทำยังไง
        line_id = request.GET.get('user_id', None)
        user = CustomUser.objects.filter(line_id=line_id).first()
        order = Order.objects.filter(user=user)
        details = [OrderDetail.objects.filter(order=order)]
        lastests_order = Order.map_object_to_list(order)
        count = len(order)
        return JsonResponse({'orders': lastests_order, 'count': 1})

    def patch(self, request):
        line_id = request.GET.get('user_id', None)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # print(body)
        menu_id = body['menu_id']
        action = body['action']
        restaurant_id = body['restaurant_id']

        print('-----------',body)
        with transaction.atomic():
            user = CustomUser.objects.filter(line_id=line_id).first()
            restaurant = Restaurant.objects.filter(id=restaurant_id).first()
            order = Order.objects.get_or_create(user=user, restaurant=restaurant)
            menu = Menu.objects.filter(id=menu_id).first()
            detail,created = OrderDetail.objects.get_or_create(menu=menu, order=order)
            if action == 'add':
                detail.quantity += 1
            elif action == 'del':
                if detail.quantity > 0:
                    detail.quantity -= 1
                else:
                    detail.delete()
        return JsonResponse({})