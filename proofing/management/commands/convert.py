from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from optparse import make_option
from proofing.models import *
from heirloom.store import models as hmodels

from heirloom import cart
import shutil,uuid
from heirloom import sampleimages

class Command(BaseCommand):

    requires_model_validation = True
    can_import_settings = True

    def handle(self, *args, **options):
        
#        for cat in hmodels.Category.objects.all():
#            c = Category()
#            c.title = cat.name
#            c.slug = cat.slug
#            c.description = cat.description
#            c.is_active = cat.is_active
#            c.meta_keywords = cat.meta_keywords
#            
#            try:
#                c.save()
#                print c,'done'
#            except:
#                print c,'already exists'
            
        
#        for pc in hmodels.PricingCategory.objects.all():
#            t = GalleryType()
#            t.title = pc.name
#            t.slug = slugify(pc.name)
#            t.description = pc.description
#            
#            try:
#                t.save()
#                print t
#            except:
#                print t,'already exists'
                
    
#        for e in hmodels.Event.objects.all():
#            g = Gallery()
#            g.title = e.name
#            g.slug = e.slug
#            g.description = e.description
#            g.is_active = e.is_active
#            g.meta_keywords = e.meta_keywords
#            
#            g.category = Category.objects.filter(slug = e.category.slug)[0]
#            g.type = GalleryType.objects.filter(slug = slugify(e.pricing_category.name))[0]
#            
#            
#            
#            try:
#                g.save()
#                print g
#            except:
#                print g,'already done'
                
         
#        for pr in hmodels.Product.objects.all():
#            p = Photo()
#            p.title = pr.name
#            p.slug = pr.slug
#            p.description = pr.description
#            p.is_active = pr.is_active
#            p.gallery = Gallery.objects.get(slug = pr.event.slug)
#            p.image = PROOFING_PATH+'/orig/'+pr.image
#            
#            src = settings.MEDIA_ROOT+hmodels.STORE_IMAGES_LOCATION_PREFIX+pr.image
#            dst = p.image.path
#            
#            try:
#                shutil.copy(src, dst)
#                print p, src,'->',dst
#            except:
#                print p,'not found'
#            
#            try:
#                p.save()
#            except:
#                pass
            
    
        
#        for ci in cart.models.CartItem.objects.all():
#            ci.product_id = Photo.objects.get(slug=ci.product.slug).id
#            #print ci
#            
#            ci.save()
#            
#        for fi in cart.models.FavoriteItem.objects.all():
#            fi.product_id = Photo.objects.get(slug=fi.product.slug).id
#            #print ci
#            
#            fi.save()   
            
        
    
        for sc in sampleimages.models.SampleCategory.objects.all():

            try:
                c = Gallery.objects.get(slug=slugify(sc.name))
            except:
                c = Gallery()
                c.title = sc.name
                c.slug = slugify(sc.name)
            
            try:
                c.category = Category.objects.get(slug='sample')
                print c,'had it'
            except:
                c.category = Category.objects.create(title="Sample", slug='sample')
                print c,'didnt have it'
            
            try:
                c.type = GalleryType.objects.get(slug='sample')
            except:
                c.type = GalleryType.objects.create(title='Sample', slug='sample')
            
            
            try:
                c.save()
                print c,'done'
            except:
                print c,'already done'
            
        
#        print [s.slug for s in Category.objects.all()]
        for sample in sampleimages.models.SampleImage.objects.all():
            s = Photo()
            print sample
            try:
                s.title = sample.name
                s.slug = slugify(sample.image)
            except:
                s.title = 'Sample'+sample.image
                s.slug = slugify('_Sample'+sample.image)
            print '-',s.slug
            s.gallery = Gallery.objects.get(slug=slugify(sample.category.name))
            
            s.type = GalleryType.objects.get(slug='sample')
            s.save()
            print s
            
            
            
            
            
            
            
            
            
            
            
#            src = settings.MEDIA_ROOT+sampleimages.models.SAMPLE_IMAGES_LOCATION_PREFIX+sample.image
#            dst = s.image.path
#            print s, src,'->',dst
#            try:
#                shutil.copy(src, dst)
#                print p, src,'->',dst
#            except:
#                print p,'not found'
#            
#            try:
#                p.save()
#            except:
#                pass
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            