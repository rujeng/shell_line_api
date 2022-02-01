from django.db import models
from line.models import CustomUser,CarBrand, Car , CarModel

# Create your models here.
class TransactionForm(models.Model):
    INITIAL = 'INITIAL'
    PROCESSING = 'PROCESSING'
    DONE = 'DONE'
    FAILED = 'FAILED'
    STATUS_CHOICES = [
        (INITIAL, 'INITIAL'),
        (PROCESSING, 'PROCESSING'),
        (DONE, 'DONE'),
        (FAILED, 'FAILED'),
    ]
    CASH = 'CASH'
    TRANSFER_BBL = 'TRANSFER_BBL'
    CREDIT_CARD_SCB = 'CREDIT_CARD_SCB'
    QR_SCB = 'QR_SCB'
    CUSTOMER_CREDIT = 'CUSTOMER_CREDIT'
    PAYMENT_CHOICES = [
        (CASH,'เงินสด'),
        (TRANSFER_BBL,'โอน_BBL'),
        (CREDIT_CARD_SCB,'เครดิตการ์ด_SCB'),
        (QR_SCB,'QR_SCB'),
        (CUSTOMER_CREDIT,'ลูกค้าเครดิต')
    ]
    branch_id = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True,null=True, related_name='user_transaction')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='car_transaction')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=INITIAL)
    appointed_date = models.DateTimeField()
    total_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    payment_method = models.CharField(blank=True, null=True,max_length=20,choices=PAYMENT_CHOICES)
    comment = models.TextField(blank=True, null=True)
    is_notify = models.BooleanField(default=False)
    is_notify_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}' if self.user else '---' 


class TransactionDetail(models.Model):
    transaction_form = models.ForeignKey(TransactionForm, related_name='sale_detail', on_delete=models.CASCADE)
    # order = models.CharField(max_length=20)
    # product_name = models.CharField(max_length=50)
    item = models.ForeignKey('Item', related_name='item', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sell_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    # total_bill = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    location_store =  models.CharField(max_length=30)
    comment =  models.CharField(max_length=50 , blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Item(models.Model):
    purchase_barcode = models.CharField(max_length=20)
    # transaction_detail = models.ForeignKey(TransactionDetail, related_name='item', on_delete=models.CASCADE, blank=True, null=True)
    barcode = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    supplier = models.CharField(max_length=50)
    main_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    sell_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    image_url = models.URLField(max_length = 200, blank=True, null=True)
    liter = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}' if self.name else '---' 


class CalculatePrice(models.Model):
    # Active = True
    # Inactive = False
    # STATUS_CHOICES = [
    #     (Active, 'ACTIVE'),
    #     (Inactive, 'INACTIVE'),
    # ]
    # brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    name =  models.CharField(max_length=30)
    series = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    num_liter = models.CharField(max_length=5)
    eco = models.BooleanField(default=False)
    bensin = models.BooleanField(default=False)
    diesel = models.BooleanField(default=False)
    rimula = models.BooleanField(default=False)
    eco_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    semi_sync_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    sync_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    premium_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ItemImage(models.Model):
    item = models.OneToOneField('Item', on_delete=models.CASCADE, primary_key=True,)
    image = models.ImageField(upload_to='items/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.item}' if self.item else '---' 