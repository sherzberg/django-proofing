from django.contrib import admin
from models import *



class DefaultAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'date_changed', 'is_active',)
    list_filter = ['date_added']
    date_hierarchy = 'date_added'
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'slug']
    list_per_page = 50

    fieldsets = (
        (None, {
            'fields': ('title', 'is_active',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('slug', 'description', 'meta_keywords', )
        }),
    )
    
    
    
class CategoryAdmin(DefaultAdmin):
    pass
    
    
    
class GalleryAdmin(DefaultAdmin):
    list_display = DefaultAdmin.list_display+('category', 'type', 'date_expires', 'admin_thumbnail',)
    list_filter = DefaultAdmin.list_filter+['date_expires']

    fieldsets = (
        (None, {
            'fields': (
                       ('title', 'is_active',),
                       ('category',),
                       ('type',),
                       ('date_expires',)
                       )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('slug', 'description', 'meta_keywords', )
        }),
    )


class GalleryTypeAdmin(DefaultAdmin):
    pass



class GalleryUploadAdmin(DefaultAdmin):
    list_display = DefaultAdmin.list_display+('gallery', 'zip_file',)
    
    fieldsets = (
        (None, {
            'fields': (
                       ('title', 'is_active',),
                       ('gallery',),
                       ('zip_file',),
                       )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('slug', 'description', 'meta_keywords', )
        }),
    )


class PhotoAdmin(DefaultAdmin):
    list_display = DefaultAdmin.list_display+('gallery', 'view_count', 'admin_thumbnail',)
    list_filter = DefaultAdmin.list_filter+['gallery']
    list_per_page = 10
    
    fieldsets = (
        (None, {
            'fields': (
                       ('title', 'is_active',),
                       ('gallery',),
                       ('image',),
                       )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('slug', 'description', 'meta_keywords', )
        }),
    )

class PhotoSizeAdmin(DefaultAdmin):
    list_display = DefaultAdmin.list_display+('width', 'height', 'quality', 'crop', 'watermark',)
    
    fieldsets = (
        (None, {
            'fields': (
                       ('title', 'is_active',),
                       ('width', 'height',),
                       ('quality',),
                       ('watermark',),
                       ('upscale',),
                       ('crop',),
                       ('pre_cache',),
                       ('increment_count',),
                       )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('slug', 'description', 'meta_keywords', )
        }),
    )
    
    
class WatermarkAdmin(DefaultAdmin):
    list_display = DefaultAdmin.list_display+('image', 'style', 'opacity',)
    
    fieldsets = (
        (None, {
            'fields': (
                       ('title', 'is_active',),
                       ('image',),
                       ('style',),
                       ('opacity',),
                       )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('slug', 'description', 'meta_keywords', )
        }),
    )




admin.site.register(Category, CategoryAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Photo, PhotoAdmin)

admin.site.register(GalleryType, GalleryTypeAdmin)
admin.site.register(GalleryUpload, GalleryUploadAdmin)

admin.site.register(PhotoSize, PhotoSizeAdmin)
admin.site.register(Watermark, WatermarkAdmin)



    