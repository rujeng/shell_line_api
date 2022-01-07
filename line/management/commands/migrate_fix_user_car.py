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
            test = 0
            for row in spamreader:
                if num == 0:
                    pass
                else:
                    full_name, mobile, brand, model, car_register, date = row
                    mobile = mobile.replace('-', '')
                    mobile = mobile[:10]
                    user = CustomUser.objects.filter(mobile_no=mobile).first()
                    if user:
                        car_register_instance = Car.objects.filter(car_register=car_register, user_id=user).first()
                        if car_register_instance:
                            print('----',full_name)
                            print('-------',car_register)
                            test += 1
                    num += 1
            print('row ----', test)
        print('uploaded success')