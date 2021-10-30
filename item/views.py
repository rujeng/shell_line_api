from django.db import models
from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.core.paginator import Paginator
from django.http import JsonResponse

from item.models import TransactionDetail, TransactionForm , CalculatePrice
from line.form import BranchForm
from line.models import CustomUser , CarBrand, Car

class TestTransactionview(View):
    
    def get(self, request):
        page = request.GET.get('page', 0)
        transactions = TransactionForm.objects.order_by('-id')
        transactions = TransactionForm.objects.filter(user__id=11911)
        result = []
        # show_list = 10
        # start_page = show_list * page
        # end_page = start_page + show_list
        # print(start_page, end_page)
        for item in transactions[:20]:
            details = []
            tran_details = item.sale_detail.all()
            for myitem in tran_details:
                details.append({'name': myitem.item.name, 'id': myitem.id})

            result.append({
                'user_id': item.user,
                'car': item.car.car_register,
                'user_name': item.user.full_name,
                'sale_id': item.id,
                'user_mobile': item.user.mobile_no,
                'result': details
            })
        
        return render(request, 'list.html', context={'form': result})


@method_decorator(csrf_exempt, name='dispatch')
class CalItemPrice(View):

    def get(self, request):
        line_id = request.GET.get('user_id', 'test1')
        car_id = request.GET.get('car_id', None)
        cars = Car.objects.filter(user_id__line_id=line_id)
        user = CustomUser.objects.filter(line_id=line_id).first()
        option = None
        car = None
        if car_id:
            car = Car.objects.filter(id = car_id , user_id__line_id=line_id).filter().first()
            option = CalculatePrice.objects.filter(brand = car.model.brand,series = car.model).first()
        context = {'cars_dropdown': cars, 'user': user,'option':option,'car': car}
        return render(request, 'calculate-price.html', context=context)
    
    def post(self, request):
        type_oil = request.GET.get("type_oil", None)
        line_id = request.GET.get('user_id', 'test1')
        car_id = request.GET.get('car_id', None)
        cars = Car.objects.filter(user_id__line_id=line_id)
        user = CustomUser.objects.filter(line_id=line_id).first()
        option = None
        if car_id:
            car = Car.objects.filter(id = car_id , user_id__line_id=line_id).filter().first()
            if not car.model or not car.model.brand:
                return JsonResponse({'ok': False, 'result': {'message' : ''} })
            option = CalculatePrice.objects.filter(brand = car.model.brand,series = car.model).first()
        price = 0
        if type_oil == 1:
            price = option.semi_sync_price
        elif type_oil == 2:
            price = option.sync_price
        elif type_oil == 3:
            price = option.premium_price

        return JsonResponse({'ok': True,'result': option})

class CalcalatePriceview(View):
    def get(self, request):
        line_id = request.GET.get("user_id", None)
        user = CustomUser.objects.filter(line_id=line_id).first()
        cars = user.car_set.all()
        brand = []
        for car in cars:
            if car.model.brand not in brand:
                brand.append(car.model.brand)
        print('br' , brand)
        list_brand = CarBrand.objects.filter(name__in = brand)
        # print('lb' , list_brand)
        list_calculate_price = CalculatePrice.objects.filter(brand__in = list_brand)
        # print('lc' , list_calculate_price)
        context = {'list_calculate_price': list_calculate_price}
        for cp in list_calculate_price:
            pass
        return render(request, 'calculate-price.html' , context = context)
    
    def post(self, request):        
        # import pdb ;pdb.set_trace()
        return JsonResponse({'ok': True})
        
        
            

