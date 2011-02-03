from django.conf import settings
from django.conf.urls.defaults import *
from models import *

class PROOFING_URL_NAMES():
    INDEX = 'proofing-index'
    CATEGORY = 'proofing-category'
    EVENT = 'proofing-event'
    PHOTO = 'proofing-photo'
    
    
urlpatterns = patterns('proofing.views',
    (r'^$','index',{}, PROOFING_URL_NAMES.INDEX),
    
    (r'^(?P<slug>[-\w]+)/$', 'show_category', {}, PROOFING_URL_NAMES.CATEGORY),
    
    #must pass slug for decorators
    (r'^gallery/(?P<slug>[-\w]+)/$', 'show_gallery', {}, PROOFING_URL_NAMES.EVENT),
    (r'^photo/(?P<slug>[-\w]+)/$', 'show_photo', {}, PROOFING_URL_NAMES.PHOTO),
    
)






