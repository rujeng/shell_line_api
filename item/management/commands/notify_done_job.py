from math import fabs
from django.core.management.base import BaseCommand, CommandError
from item.models import TransactionForm
from line.models import LineMessage,LineOfficial
from line.line_service import Line
from line.message import Message
from datetime import date,datetime,time,timedelta

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        return

    def is_date_notify(self, apoint_date):
        today = date.today()
        print(apoint_date.date())
        print(today)
        if(apoint_date.date() == today):
            return True
        return False

    def get_date_today(self):
        today = date.today()
        return today
    
    def handle(self, *args, **options):
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())
        transactions = TransactionForm.objects.filter(status=TransactionForm.DONE,is_notify_done=False,appointed_date__range=(today_start,today_end))
        line = Line()
        print('---- start notify done job ----')
        print('tran count :',transactions.count())
        for tran in transactions:
            print('tran id :',tran.id)
            if(self.is_date_notify(tran.appointed_date) and tran.branch_id):
                line_message = LineMessage.objects.filter(id=tran.branch_id).first()
                branch_name = LineOfficial.objects.filter(id=tran.branch_id).first()
                tran_details = tran.sale_detail.all()
                print('tran detail count : ' , tran_details.count())
                if tran.user.line_id and line_message and branch_name and tran_details.count() > 0:
                    meta_data = {'line_id': tran.user.line_id,'branch_name':branch_name}
                    channel_access_tk = line_message.channel_access_token
                    message = Message()
                    if tran.branch_id == 1 or tran.branch_id == 2:
                       message_job = message.makemessage_job_done(meta_data,tran)
                    elif tran.branch_id == 3:
                       message_job = message.makemessage_job_done_B3(meta_data,tran)
                    res = line.push_message(channel_access_token=channel_access_tk, message_data=message_job)
                    print('res ok : ',res['ok'])
                    if res['ok'] == True:
                        tran.is_notify_done = True
                        tran.save(update_fields=['is_notify_done'])
        print('---- end notify done job ----')
            

    

