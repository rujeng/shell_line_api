from django.shortcuts import render
from django.views.generic import View

from delivery.models import MenuDetail, OrderTrans, OrderDetail

class HistorySeller(View):

    def get(self,request,pk):
        ordertrans = OrderTrans.objects.filter(id=pk)
        if not ordertrans[0]:
            return render(request, 'failed.html')
        order_detail_list = OrderDetail.objects.filter(ordertrans=ordertrans[0]).order_by('menu__restaurant_id')
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
        context = {'result': tmp,'ordertrans_id':ordertrans[0]}
        return render(request, 'order_history_seller.html',context=context)

    def mapping_payment_method(self,payment_method):
        str_payment_method = ""
        if payment_method == '1':
            str_payment_method = "เงินสด"
        elif payment_method == '2':
            str_payment_method = "โอนเงิน"
        return str_payment_method
