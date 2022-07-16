from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View, DetailView, detail
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.shortcuts import redirect

from delivery.models import Menu, MenuDetail, Restaurant, OrderTrans, OrderDetail, LocationUser
from line.models import CustomUser,LineMessage , LineOfficial
from line.line_service import Line
from delivery.line_message import line_message



class AdminView(View):

    def get(self, request):
        #init_orders_trans_list = OrderTrans.objects.filter(status=OrderTrans.INITIAL).order_by('-pk')
        pro_orders_trans_list = OrderTrans.objects.filter(status=OrderTrans.PROCESSING).order_by('-pk')
        confirm_orders_trans_list = OrderTrans.objects.filter(status=OrderTrans.CONFIRM).order_by('-pk')
        done_orders_trans_list = OrderTrans.objects.filter(status=OrderTrans.DONE).order_by('-pk')
        reject_orders_trans_list = OrderTrans.objects.filter(status=OrderTrans.REJECT).order_by('-pk')
        fail_orders_trans_list = OrderTrans.objects.filter(status=OrderTrans.FAILED).order_by('-pk')
        context = {'pro_orders_trans_list':pro_orders_trans_list,
                    'confirm_orders_trans_list':confirm_orders_trans_list,
                    'done_orders_trans_list':done_orders_trans_list,
                    'reject_orders_trans_list':reject_orders_trans_list,
                    'failed_orders_trans_list':fail_orders_trans_list,
                    }
        return render(request, 'admin_view.html', context=context)

@method_decorator(csrf_exempt, name='dispatch')
class AdminViewDetail(View):

    def get(self,request,pk):
        ordertrans = OrderTrans.objects.filter(id=pk)
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
        return render(request, 'admin_view_detail.html',context=context)
    
    def post(self,request,pk):
        distance = request.POST.get('distance', None)
        distance_price = request.POST.get('distance_price', None)
        status = request.POST.get('status', None)
        comment = request.POST.get('comment', None)
        ordertrans = OrderTrans.objects.filter(id=pk).first()
        location_user = LocationUser.objects.filter(id=ordertrans.location_user.id).first()
        order_detail_list = OrderDetail.objects.filter(ordertrans=ordertrans)
        result_dict = dict()
        total_price_food = 0
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
                    total_price_food += item.on_top_price
                details = MenuDetail.map_to_list(menu_detail_obj)
            detail_dict = {'menu': order.menu.name, 'price': order.menu.price, 'quantity': order.quantity, 'details': details, 'description': order.description}
            total_price_food += order.quantity * order.menu.price
        line = Line()
        message = line_message()
        line_id = ordertrans.user.line_id
        branch_name = LineOfficial.objects.filter(id=ordertrans.branch_id).first()
        lineMessage = LineMessage.objects.filter(id=ordertrans.branch_id).first()
        channel_access_token = lineMessage.channel_access_token
        meta_dat = {
            'line_id':line_id,
            'branch_name':branch_name,
            'distance':distance,
            'distance_price':distance_price,
            'total_price_food':total_price_food,
            'comment':comment}
        if status == '3':
            message_data_push_noti = message.confirm_message(meta_dat=meta_dat,tran=ordertrans)
            res = line.push_message(
                    meta_dat, channel_access_token,message_data_push_noti)
            if res['ok']:
                ordertrans.status = OrderTrans.CONFIRM
                location_user.distance = distance
                ordertrans.distance_price = distance_price
                location_user.distance_price = distance_price
                ordertrans.description = comment
                ordertrans.save()
                location_user.save()
        elif status == '5':
            message_data_push_noti = message.reject_message(meta_dat=meta_dat,tran=ordertrans)
            res = line.push_message(
                    meta_dat, channel_access_token,message_data_push_noti)
            if res['ok']:
                ordertrans.status = OrderTrans.REJECT
                ordertrans.save()
        return redirect(f'/delivery/admin')

    def mapping_payment_method(self,payment_method):
        str_payment_method = ""
        if payment_method == '1':
            str_payment_method = "เงินสด"
        elif payment_method == '2':
            str_payment_method = "โอนเงิน"
        return str_payment_method
    