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
        day, month, year = ''.join(date).split('/')
        # import pdb ; pdb.set_trace()
        if len(day) == 1:
            day = '0'+day
        if len(month) == 1:
            month = '0'+month
        year = str(int(year) - 543)
        datetime_format = f'{year}/{month}/{day}'
        # import pdb ; pdb.set_trace()
        return datetime.strptime(datetime_format, '%Y/%m/%d')

    @transaction.atomic
    def handle(self, *args, **options):
        print('uploading please wait ....')
        PROJECT_PATH = Path(__file__).resolve().parent
        BASE = os.path.join(PROJECT_PATH.parent, 'commands')
        file_path = BASE + '\\transaction.csv'
        # import pdb ; pdb.set_trace()
        with open(file_path, newline='', encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile)
            num = 0
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
                    # import pdb ; pdb.set_trace()
                    if car:
                        user = car.user_id
                        # user_id = car.user_id.id
                        tran, is_existed = TransactionForm.objects.get_or_create(
                            car=car, user=user, status=TransactionForm.DONE, appointed_date=self.parse_string_to_datetime(appointed_date),
                            comment=comment, total_price=total_price
                        )
                        item = Item.objects.filter(barcode=barcode).first()
                        result.append(TransactionDetail(
                            transaction_form=tran, item=item, quantity=quantity, sell_price=sale_price,
                            location_store=location_store
                        ))
                    else:
                        print(car_register)
                num += 1
            
            print('row------', num)
            TransactionDetail.objects.bulk_create(result)
        print('uploaded success')