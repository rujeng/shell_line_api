from django.core.management.base import BaseCommand, CommandError
from item.models import CalculatePrice
import csv
import os
from pathlib import Path

from line.models import CarBrand, CarModel

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        return

    def handle(self, *args, **options):
        print('uploading please wait ....')
        PROJECT_PATH = Path(__file__).resolve().parent
        BASE = os.path.join(PROJECT_PATH.parent, 'commands')
        file_path = BASE + '/calculate_price.csv'
        with open(file_path, newline='', encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile)
            num = 0
            result = []
            for row in spamreader:
                brand,name,series,num_liter,eco,bensin,diesel,rimula,eco_price,semi_sync_price,sync_price,premium_price = row
                brand_db,is_exist = CarBrand.objects.get_or_create(name = brand)
                series_db,is_exist = CarModel.objects.get_or_create(brand = brand_db,name = series)
                eco_price = float(eco_price) if eco_price else 0
                semi_sync_price = float(semi_sync_price) if semi_sync_price else 0
                sync_price = float(sync_price) if sync_price else 0
                premium_price = float(premium_price) if premium_price else 0
                result.append(CalculatePrice(name=name,series=series_db,num_liter=num_liter,eco=bool(eco),bensin=bool(bensin),
                                            diesel=bool(diesel),rimula=bool(rimula),eco_price=eco_price,semi_sync_price=semi_sync_price,
                                            sync_price=sync_price,premium_price=premium_price
                ))
                num += 1
            CalculatePrice.objects.bulk_create(result)
        print('uploaded success')