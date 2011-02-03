from django.core.management.base import BaseCommand, CommandError

from proofing.models import *


CATEGORIES = 'Sports Family Other'.split()
GALLERYTYPES = 'Regular Senior Special'.split()

PHOTOSIZES = {'regular': (600,600),
              'thumb': (200,150)
              }




class Command(BaseCommand):
    args = ""
    help = 'test'

    def handle(self, *args, **options):
        
        print Gallery.active.all()