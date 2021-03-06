from django.db import models
from line.models import LineOfficial, CustomUser
# Create your models here.

class Restaurant(models.Model):
    line_official = models.ForeignKey(LineOfficial, related_name='restaurant', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_menu_list(restaurants):
        result = []
        for restaurant in restaurants:
            menus = Menu.objects.filter(restaurant=restaurant).all()
            menus = Menu.map_object_to_list(menus)
            result.append({
                'name': restaurant.name,
                'menus': menus,
                'id': restaurant.id
            })
        return result


class Menu(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    # detail = models.TextField(null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def map_object_to_list(object_list):
        result = []
        for item in object_list:
            details = MenuDetail.objects.filter(menu=item)
            detail_result = []
            for detail in details:
                detail_result.append({
                    'name': detail.detail,
                    'price': detail.on_top_price
                })
            result.append({
                'name': item.name,
                'price': item.price,
                'id': item.id,
                'res_id': item.restaurant.id,
                'details': detail_result
            })
        return result


class MenuDetail(models.Model):
    menu = models.ForeignKey('Menu', related_name='menu_detail', on_delete=models.CASCADE)
    detail = models.CharField(max_length=50)
    on_top_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    INITIAL = '1'
    PROCESSING = '2'
    DONE = '3'
    FAILED = '4'
    STATUS_CHOICES = [
        (INITIAL, 'INITIAL'),
        (PROCESSING, 'PROCESSING'),
        (DONE, 'DONE'),
        (FAILED, 'FAILED'),
    ]
    restaurant = models.ForeignKey('Restaurant', related_name='order', on_delete=models.CASCADE)
    total_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    user =  models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=INITIAL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)
    
    def map_object_to_list(object_list):
        result = []
        for order in object_list:
            result.append({
                'status': order.status,
                'id': order.id,
                'detail': order.total_price,
            })
        return result


class OrderDetail(models.Model):
    order = models.ForeignKey('Order', related_name='order_detail', on_delete=models.CASCADE)
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    description = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.menu)

    def get_detail(order):
        result = []
        details = OrderDetail.objects.filter(order=order)
        for detail in details:
            # import pdb ; pdb.set_trace()
            result.append({
                'name': detail.name
            })
        return result