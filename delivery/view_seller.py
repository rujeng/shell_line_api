from django.shortcuts import render
from django.views.generic import View

from delivery.models import MenuDetail, OrderTrans, OrderDetail

class HistorySeller(View):

    def get(self,request,pk):
        ordertrans = OrderTrans.objects.filter(id=pk)
        if not ordertrans[0]:
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
        print(context)
        return render(request, 'order_history_seller.html',context=context)

    def mapping_payment_method(self,payment_method):
        str_payment_method = ""
        if payment_method == '1':
            str_payment_method = "เงินสด"
        elif payment_method == '2':
            str_payment_method = "โอนเงิน"
        return str_payment_method
