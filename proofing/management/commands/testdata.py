from django.core.management.base import BaseCommand, CommandError

from proofing.models import *


CATEGORIES = 'Sports Family Other'.split()
GALLERYTYPES = 'Regular Senior Special'.split()

PHOTOSIZES = {'regular': (600,600),
              'thumb': (200,150)
              }

class Command(BaseCommand):
    args = ""
    help = 'testdata'

    def handle(self, *args, **options):
        for c in CATEGORIES:
            cat = Category(title=c,slug=c.lower())
            cat.save()
            
        print 'Categories Done'
        for gt in GALLERYTYPES:
            gtype = GalleryType(title=gt,slug=gt.lower())
            gtype.save()
            
        print 'GalleryTypes Done'
        
        for ps,size in PHOTOSIZES.items():
            photosize = PhotoSize(title=ps,
                                  slug=ps.lower(),
                                  height=size[1],
                                  width=size[0]
                                  )
            photosize.save()
            
        print 'PhotoSizes Done'
        
            
            

