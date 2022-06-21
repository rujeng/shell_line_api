from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View, DetailView, detail
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.shortcuts import redirect

from delivery.models import Menu, MenuDetail, Restaurant, OrderTrans, OrderDetail, LocationUser
from line.models import CustomUser


class AdminView(View):

    def get(self, request):
        init_orders_trans_list = OrderTrans.objects.filter(status=OrderTrans.INITIAL).order_by('-pk')
        pro_orders_trans_list = OrderTrans.objects.filter(status=OrderTrans.PROCESSING).order_by('-pk')
        done_orders_trans_list = OrderTrans.objects.filter(status=OrderTrans.DONE).order_by('-pk')
        fail_orders_trans_list = OrderTrans.objects.filter(status=OrderTrans.FAILED).order_by('-pk')
        context = {'init_orders_trans_list': init_orders_trans_list}
        return render(request, 'admin_view.html', context=context)