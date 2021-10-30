from django.core.management.base import BaseCommand, CommandError
from item.models import Item
import csv
import os
from pathlib import Path

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        return

    def handle(self, *args, **options):
        print('uploading please wait ....')
        PROJECT_PATH = Path(__file__).resolve().parent
        BASE = os.path.join(PROJECT_PATH.parent, 'commands')
        file_path = BASE + '/item.csv'
        with open(file_path, newline='', encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile)
            num = 0
            result = []
            for row in spamreader:
                if num == 0:
                    pass
                else:
                    item_id,item_no,item_barcode,name,category,supplier,cost,price,image,timestamp = row
                    cost = float(cost) if cost else 0
                    price = float(price) if price else 0
                    result.append(Item(
                        purchase_barcode=item_no, barcode=item_barcode, name=name, category=category,
                        supplier=supplier, main_price=float(cost), sell_price=float(price), image_url=image 
                    ))
                num += 1
            Item.objects.bulk_create(result)
        print('uploaded success')