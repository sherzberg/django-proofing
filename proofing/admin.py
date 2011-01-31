from django.contrib import admin
import django.forms as forms
from django.db import models

from models import *

admin.site.register(Category)
admin.site.register(GalleryType)
admin.site.register(GalleryUpload)
admin.site.register(Gallery)
admin.site.register(Photo)
admin.site.register(PhotoSize)
admin.site.register(Watermark)
    