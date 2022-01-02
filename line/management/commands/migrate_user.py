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
                    full_name, mobile, brand, model, car_register, date = row
                    mobile = mobile.replace('-', '')
                    mobile = mobile[:10]
                    user, is_existed = CustomUser.objects.get_or_create(mobile_no=mobile)
                    car_register_instance = Car.objects.filter(car_register=car_register, user_id=user).first()
                    model = CarModel.objects.filter(name=model).first()
                    if car_register_instance:
                        print('-------',car_register)
                        continue
                    else:
                        if model:  # check existed brand and model
                            Car.objects.create(user_id=user, model=model, car_register=car_register)
                        else:
                            Car.objects.create(user_id=user, car_register=car_register, status=False)
                num += 1
            print('row ----', num)
        print('uploaded success')