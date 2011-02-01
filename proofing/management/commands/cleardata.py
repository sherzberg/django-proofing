from django.core.management.base import BaseCommand, CommandError

from proofing.models import *


CATEGORIES = ('Sports','Family','Other',)


class Command(BaseCommand):
    args = ""
    help = 'testdata'

    def handle(self, *args, **options):
        answer = raw_input('Are you sure? (y,n)')
        if answer[0].lower() == 'y':
            Category.objects.all().delete()
            GalleryType.objects.all().delete()
            PhotoSize.objects.all().delete()
        else:
            print 'doing nothing'
            return
        
        print 'done'
            
            





        
