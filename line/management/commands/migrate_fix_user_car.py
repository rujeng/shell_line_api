from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from line.models import CustomUser, Car , CarBrand, CarModel
from item.models import TransactionForm
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
            count_car = 0
            count_tran = 0
            for row in spamreader:
                if num == 0:
                    pass
                else:
                    full_name, mobile, brand, model, car_register, date = row
                    mobile = mobile.replace('-', '')
                    mobile = mobile[:10]
                    user = CustomUser.objects.filter(mobile_no= mobile).first()
                    if user:
                        car_register_instance = Car.objects.filter(car_register=car_register, user_id=user).first()
                        if car_register_instance:
                            # tran = TransactionForm.objects.filter(car_id = car_register_instance)
                            # if tran:
                            #     for tr in tran:
                            #         print('--',tr.id)
                            # print('----',full_name)
                            # print('-------',car_register)
                            test += 1
                        else:
                            ucar = Car.objects.filter(car_register=car_register).first()
                            if ucar :
                                ucar.user_id_id = user
                                ucar.save(update_fields=['user_id_id'])
                                trans = TransactionForm.objects.filter(car_id = ucar)
                                for tran in trans:
                                    tran.user_id = user
                                    tran.save(update_fields=['user_id'])
                                    count_tran += 1
                                # if tran:
                            count_car += 1         
                            # if ucar:
                            #     ucar.user_id = user
                            #     ucar.update(update_fields=['user_id'])
                            #     tran = TransactionForm.objects.filter(car_id = ucar)
                            #     if tran:
                            #         tran.user_id = user
                            #         tran.update(update_fields=['user_id'])
                num += 1
            print('row car ----', count_car)
            print('row tran ----', count_tran)
        print('uploaded success')