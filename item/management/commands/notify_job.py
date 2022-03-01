from django.core.management.base import BaseCommand, CommandError
from item.models import TransactionForm
from line.models import LineMessage
from line.line_service import Line
from line.message import Message
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        return

    def is_date_notify(self, current_date):
        next_4_month = current_date + relativedelta(months=4)
        today = datetime.today()
        if today.month == next_4_month.month and today.day == next_4_month.day:
            return True
        return False
    
    def handle(self, *args, **options):
        transactions = TransactionForm.objects.filter(status=TransactionForm.DONE,is_notify=False)
        line = Line()
        print('---- start notify 4 months job ----')
        print('tran count :',transactions.count())
        for tran in transactions:
            if self.is_date_notify(tran.appointed_date) and tran.user.line_id and tran.branch_id :
                tran_lstdate = TransactionForm.objects.filter(car=tran.car).latest('appointed_date')
                if tran.id == tran_lstdate.id:
                    meta_data = {'line_id': tran.user.line_id}
                    line_message = LineMessage.objects.filter(id=tran.branch_id).first()
                    if line_message:
                        channel_access_tk = line_message.channel_access_token
                        message = Message()
                        message_job = message.makemessage_job_4_month(meta_data,tran)
                        res = line.push_message(channel_access_token=channel_access_tk, message_data=message_job)
                        print('res ok : ',res['ok'])
                        if res['ok'] == True:
                            tran.is_notify = True
                            tran.save(update_fields=['is_notify'])
                else:
                    tran.is_notify = True
                    tran.save(update_fields=['is_notify'])
        print('---- end notify done job ----')
