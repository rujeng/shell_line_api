from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
# from inventory.models import InventoryCount
from inventory.models import InventoryCount
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        return

    def checkdate(self, last_date):
        seven_days_ago = datetime.today() - timedelta(days = 7)
        if(seven_days_ago.date() > last_date.date()):
            return True
        return False
    
    def Delete_Data_Stock_Count(self,branch_id_in):
        try:
            print("branch : ",branch_id_in)
            last_inventory_count = InventoryCount.objects.filter(branch_id=branch_id_in).latest('created_at')
        except ObjectDoesNotExist:
            last_inventory_count = None
            print('none data')
            return
        if last_inventory_count and self.checkdate(last_inventory_count.updated_at):
            try:
                record = InventoryCount.objects.filter(branch_id = branch_id_in)
                record.delete()
                print("Record deleted successfully!")
            except:
                print("Record doesn't exists")
            return
        print("Record doesn't match time")
        return

    def handle(self, *args, **options):
        self.Delete_Data_Stock_Count(1)
        self.Delete_Data_Stock_Count(2)
        self.Delete_Data_Stock_Count(3)
        return
       