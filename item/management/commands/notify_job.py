from django.core.management.base import BaseCommand, CommandError
from item.models import TransactionForm
from line.line_service import Line

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        return

    def is_date_notify(self, date):
        return True
    
    def handle(self, *args, **options):
        transactions = TransactionForm.objects.filter(is_notify=False)
        line = Line()
        for tran in transactions:
            if self.is_date_notify(tran.appointed_date):
                line.push_message(channel_access_token='ee', message_data={})
                tran.is_notify = True
                tran.save(update_fields=['is_notify'])


    

