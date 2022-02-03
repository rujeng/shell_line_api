from math import fabs
from django.core.management.base import BaseCommand, CommandError
from item.models import TransactionForm
from line.models import LineMessage,LineOfficial
from line.line_service import Line
from line.message import Message
from datetime import date

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        return

    def is_date_notify(self, apoint_date):
        today = date.today()
        today = today.strftime("%d/%m/%Y")
        ap_date = apoint_date.strftime("%d/%m/%Y")
        print(today)
        print(ap_date)
        if(ap_date == today):
            return True
        return False
    
    def handle(self, *args, **options):
        transactions = TransactionForm.objects.filter(status=TransactionForm.DONE,is_notify_done=False)
        line = Line()
        for tran in transactions:
            if(self.is_date_notify(tran.appointed_date)):
                line_message = LineMessage.objects.filter(id=tran.branch_id).first()
                branch_name = LineOfficial.objects.filter(id=tran.branch_id).first()
                if tran.user.line_id and line_message and branch_name:
                    meta_data = {'line_id': tran.user.line_id,'branch_name':branch_name}
                    channel_access_tk = line_message.channel_access_token
                    message = Message()
                    message_job = message.makemessage_job_done(meta_data,tran)
                    # print(message_job)
                    line.push_message(channel_access_token=channel_access_tk, message_data=message_job)
                    tran.is_notify_done = True
                    tran.save(update_fields=['is_notify_done'])
            return
            

    

