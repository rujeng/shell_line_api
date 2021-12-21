from django.core.management.base import BaseCommand, CommandError
from item.models import TransactionForm
from line.models import LineMessage
from line.line_service import Line
from line.message import Message

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        return

    def is_date_notify(self, date):
        return True
    
    def handle(self, *args, **options):
        transactions = TransactionForm.objects.filter(status=TransactionForm.DONE)
        line = Line()
        for tran in transactions:
            meta_data = {'line_id': tran.user.line_id}
            line_message = LineMessage.objects.filter(id=tran.branch_id).first()
            channel_access_tk = line_message.channel_access_token
            message = Message()
            message_job = message.makemessage_job_4_mount(meta_data)
            line.push_message(channel_access_token=channel_access_tk, message_data=message_job)


    

