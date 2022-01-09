from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from line.models import CustomUser, Car
from item.models import TransactionForm, TransactionDetail, Item
import csv
import os
from pathlib import Path
from datetime import datetime

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        return
        # parser.add_argument('poll_ids', nargs='+', type=int)
    
    def parse_string_to_datetime(self, date_string):
        
        date, time = date_string.split(' ')
        # import pdb ; pdb.set_trace()
        month,day , year = ''.join(date).split('/')
        # import pdb ; pdb.set_trace()
        if len(day) == 1:
            day = '0'+day
        if len(month) == 1:
            month = '0'+month
        year = str(int(year) - 543)
        datetime_format = f'{year}/{month}/{day}'
        # print("datetime 1 : ", datetime_format  )
        # print("datetime 2 : ", datetime.strptime(datetime_format, '%Y/%m/%d'))

        # import pdb ; pdb.set_trace()
        return datetime.strptime(datetime_format, '%Y/%m/%d')

    @transaction.atomic
    def handle(self, *args, **options):
        print('uploading please wait ....')
        PROJECT_PATH = Path(__file__).resolve().parent
        BASE = os.path.join(PROJECT_PATH.parent, 'commands')
        file_path = BASE + '/transaction.csv'
        # import pdb ; pdb.set_trace()
        with open(file_path, newline='', encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile)
            num = 0
            no_car = 0
            num_update = 0
            result = []
            for row in spamreader:
                if num == 0:
                    pass
                else:
                    car_register = row[1]
                    mobile = row[3].replace('-', '')
                    total_price = row[4]
                    appointed_date = row[5]
                    comment = row[6]
                    barcode = row[7]
                    product_name = row[8]
                    quantity = row[9]
                    # sale_price = row[9]
                    sale_price = row[10]
                    quantity_product_price = row[11]
                    item_created_date = row[12]
                    location_store = row[13]
                    
                    quantity = int(quantity) if quantity else 0
                    sale_price = float(sale_price) if sale_price else 0
                    car = Car.objects.filter(car_register=car_register).first()
                    list_barcode = ['90915YZZC5 6','90915YZZD2 4','15208ED50A','7443978','90915YZZD2 3']
                    if barcode in list_barcode:
                        if barcode == '90915YZZC5 6':
                            barcode = '90915YZZC5  6'
                        elif barcode == '90915YZZD2 4':
                            barcode = '90915YZZD2  4'
                        elif barcode == '15208ED50A':
                            barcode = '15208EB70D'
                        elif barcode == '90915YZZD2 3':
                            barcode = '90915YZZD2  3'
                        elif barcode == '7443978':
                            barcode == '07443978'
                        item = Item.objects.filter(barcode=barcode).first()
                        if car:
                            user = car.user_id
                            # user_id = car.user_id.id
                            tran = TransactionForm.objects.filter(
                                car_id=car
                            )
                            if tran:
                                for tr in tran:
                                    trde = TransactionDetail.objects.filter(
                                    transaction_form_id=tr.id)
                                    for td in trde:
                                        if not td.item_id:
                                            td.item_id = item
                                            td.save(update_fields=['item_id'])
                                            num_update +=1
                                            print(td.id)
                        else:
                            no_car += 1
                            # print(car_register)
                num += 1
            
            print('row------', num)
            print('no car register', no_car)
            print('item id update row ', num_update)
            TransactionDetail.objects.bulk_create(result)
        print('uploaded success')