from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from line.models import CustomUser, Car , CarBrand, CarModel
import csv
import os
from pathlib import Path

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        return
        # parser.add_argument('poll_ids', nargs='+', type=int)
    
    def handle(self, *args, **options):
        print('uploading please wait ....')
        PROJECT_PATH = Path(__file__).resolve().parent
        BASE = os.path.join(PROJECT_PATH.parent, 'commands')
        file_path = BASE + '/customuser.csv'
        with open(file_path, newline='', encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile)
            num = 0
            for row in spamreader:
                if num == 0:
                    pass
                else:
                    customer_id, full_name, mobile, brand, model, car_register, date, ref = row
                    mobile = mobile.replace('-', '')
                    mobile = mobile[:10]
                    user, is_existed = CustomUser.objects.get_or_create(mobile_no=mobile, full_name=full_name)
                    brand = CarBrand.objects.filter(name=brand).first()
                    if brand:  # check existed brand and model
                        if CarModel.objects.filter(brand=brand, name=model).exists():
                            Car.objects.create(user=user, brand=brand, car_register=car_register)

                num += 1
            print('row ----', num)
        print('uploaded success')