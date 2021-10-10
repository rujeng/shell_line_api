from django.core.management.base import BaseCommand, CommandError
from line.models import CarBrand

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        return

    def handle(self, *args, **options):
        print('uploading please wait ....')
        list_brand = [  'Isuzu',
                        'Hyundai',
                        'Mazda',
                        'Mitsubishi',
                        'Nissan',
                        'Suzuki',
                        'Subaru',
                        'Toyota',
                        'Chevrolet',
                        'Ford',
                        'Honda',
                        'Land Rover',
                        'Kia',
                        'MG'  ]
        row = 0
        for brand in list_brand:
                CarBrand.objects.create(name = f'{brand}')
                row += 1
        print('uploaded success total row : ' , row)