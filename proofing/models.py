import os
import random
import uuid
import zipfile
from datetime import datetime, timedelta

from django.db import models
from django.db.models.signals import post_init
from django.db.models.query import QuerySet
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_str, force_unicode
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile

#from utils import EXIF
#from utils.watermark import apply_watermark

try:
    import Image
    import ImageFile
    import ImageFilter
    import ImageEnhance
    ImageFile.MAXBLOCK = 1000000 # default is 64k
    #http://mail.python.org/pipermail/image-sig/1999-August/000816.html
except ImportError:
    try:
        from PIL import Image
        from PIL import ImageFile
        from PIL import ImageFilter
        from PIL import ImageEnhance
    except ImportError:
        raise ImportError('Django-Proofing was unable to import the Python Imaging Library. Please confirm it`s installed and available on your current Python path.')


from urls import PROOFING_URL_NAMES 
from utils import EXIF
from utils.reflection import add_reflection
from utils.watermark import apply_watermark

PROOFING_PATH = getattr(settings, 'PROOFING_PATH','proofing')
PROOFING_DEFAULT_THUMB = getattr(settings, 'PROOFING_DEFAULT_THUMB',settings.MEDIA_URL+'notfound.jpg')
IMAGE_FIELD_MAX_LENGTH=100
PROOFING_DEFAULT_THUMB_SIZE = getattr(settings, 'PROOFING_DEFAULT_THUMB_SIZE',(200,150))

### Choices

# Quality options for JPEG images
JPEG_QUALITY_CHOICES = (
    (30, _('Very Low')),
    (40, _('Low')),
    (50, _('Medium-Low')),
    (60, _('Medium')),
    (70, _('Medium-High')),
    (80, _('High')),
    (90, _('Very High')),
)

WATERMARK_STYLE_CHOICES = (
    ('tile', _('Tile')),
    ('scale', _('Scale')),
)

# choices for new crop_anchor field in Photo
CROP_ANCHOR_CHOICES = (
    ('top', _('Top')),
    ('right', _('Right')),
    ('bottom', _('Bottom')),
    ('left', _('Left')),
    ('center', _('Center (Default)')),
)

def randomFilename(filename):
    ext = filename[filename.rfind("."):]
    return str(uuid.uuid4())+ext


class CategoryManager(models.Manager):
    def get_query_set(self):
        objects = super(CategoryManager, self).get_query_set()
        objects.filter(is_active=True)
        objects.filter(gallery__in=Gallery.active.all())
        return objects.distinct()
    
class Category(models.Model):
    date_added = models.DateTimeField(_('date published', default=datetime.now()))
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(_('title'), max_length=100, unique=True)
    title_slug = models.SlugField(_('title slug'), unique=True, help_text=_('A "slug" is a unique URL-friendly title for an object'))
    description = models.TextField(_('description'), blank=True)
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField(_('meta keywords'), max_length=255, help_text=_('Comma-delimited set of SEO keywords for meta tag. ex: ifa,var,varsity,fb,football,...'), blank=True)
    
    objects = models.Manager()
    active = CategoryManager()
    
    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        
    def __unicode__(self):
        return self.title
    
    def __str__(self):
        return self.__unicode__()
    
    def get_absolute_url(self):
        return reverse(PROOFING_URL_NAMES.CATEGORY, args=[self.title_slug])

    def get_thumb_url(self):
        if len(Gallery.active.filter(category=self)) > 0:
            return Gallery.active.filter(category=self)[0].get_thumb_url()
        else:
            return PROOFING_DEFAULT_THUMB

class GalleryType(models.Model):
    date_added = models.DateTimeField(_('date published', default=datetime.now()))
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(_('title'), max_length=100, unique=True)
    title_slug = models.SlugField(_('title slug'), unique=True, help_text=_('A "slug" is a unique URL-friendly title for an object'))
    description = models.TextField(_('description'), blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        verbose_name = _('gallery type')
        verbose_name_plural = _('gallery types')

    def __unicode__(self):
        return self.title
    
class GalleryManager(models.Manager):
    def get_query_set(self):
        objects = super(GalleryManager, self).get_query_set()
        objects.filter(is_active=True)
        #objects.exclude(users__in=User.objects.all())
        objects.filter(date_expires__lt=datetime.now())

        return objects

#    def filter(self, *args, **kwargs):
#        user = kwargs.get('user',None)
#        if user:
#            if user.is_authenticated:
#                if user.is_superuser:
#                    kwargs.pop('user')
#            else:
#                return QuerySet()
#        return self.get_query_set().filter(*args, **kwargs)
    
class Gallery(models.Model):
    date_added = models.DateTimeField(_('date published', default=datetime.now()))
    updated_at = models.DateTimeField(_('date updated', default=datetime.now()))
    title = models.CharField(_('title'), max_length=100, unique=True)
    title_slug = models.SlugField(_('title slug'), unique=True, help_text=_('A "slug" is a unique URL-friendly title for an object'))
    description = models.TextField(_('description'), blank=True)
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField(_('met _keywords'), max_length=255, help_text=_('Comma-delimited set of SEO keywords for meta tag. ex: cars, balloons, sunsets,...'), blank=True)
    
    category = models.ForeignKey(Category)
    #type could be a many to many field??? could also add an options field
    type = models.ForeignKey(GalleryType)
    users = models.ManyToManyField(User,blank=True)
    date_expires = models.DateTimeField(_('date expires'), blank=True)
    
    objects = models.Manager()
    active = GalleryManager()
    
    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')
        
    def __unicode__(self):
        return self.title
    
    def __str__(self):
        return self.__unicode__()
    
    def get_absolute_url(self):
        return reverse(PROOFING_URL_NAMES.EVENT, args=[self.title_slug])
    
    def is_users(self):
        if len(self.users.all()) > 0:
            return True
        else:
            return False
    
    @property
    def is_expired(self):
        if not date_expired:
            return False
        else:
            return self.date_expires < datetime.now()
    
    def is_my_event(self, user):
        if user.is_superuser: return True
        if user.is_anonymous and not self.is_users(): return True
        if self in user.event_set.all(): return True
        if not user.is_anonymous:
            if self in user.event_set.all(): return True
        return False
    
    def get_thumb_url(self):
        if len(Photo.objects.filter(gallery=self)):
            return Photo.objects.all()[0].get_thumb_url()
        else:
            return PROOFING_DEFAULT_THUMB


class GalleryUpload(models.Model):
    zip_file = models.FileField(_('images file (.zip)'), upload_to=PROOFING_PATH+"/uploads",
                                help_text=_('Select a .zip file of images to upload into a new Gallery.'))
    gallery = models.ForeignKey(Gallery, null=True, blank=True, help_text=_('Select a gallery to add these images to. leave this empty to create a new gallery from the supplied title.'))
    title = models.CharField(_('title'), max_length=75, help_text=_('All photos in the gallery will be given a title made up of the gallery title + a sequential number.'))
    description = models.TextField(_('description'), blank=True, help_text=_('A description of this Gallery.'))
    meta_keywords = models.CharField(_('met _keywords'), max_length=255, help_text=_('Comma-delimited set of SEO keywords for meta tag. ex: cars, balloons, sunsets,...'), blank=True)
    
    class Meta:
        verbose_name = _('gallery upload')
        verbose_name_plural = _('gallery uploads')

    def save(self, *args, **kwargs):
        super(GalleryUpload, self).save(*args, **kwargs)
        gallery = self.process_zipfile()
        #super(GalleryUpload, self).delete()
        return gallery

    def process_zipfile(self):
        if os.path.isfile(self.zip_file.path):
            # TODO: implement try-except here
            zip = zipfile.ZipFile(self.zip_file.path)
            bad_file = zip.testzip()
            if bad_file:
                raise Exception('"%s" in the .zip archive is corrupt.' % bad_file)
            count = 1
            if self.gallery:
                gallery = self.gallery
            else:
                gallery = Gallery.objects.create(title=self.title,
                                                 title_slug=slugify(self.title),
                                                 description=self.description,
                                                 meta_keywords=self.meta_keywords
                                                 )
            from cStringIO import StringIO
            for filename in sorted(zip.namelist()):
                if filename.startswith('__'): # do not process meta files
                    continue
                data = zip.read(filename)
                if len(data):
                    try:
                        # the following is taken from django.newforms.fields.ImageField:
                        #  load() is the only method that can spot a truncated JPEG,
                        #  but it cannot be called sanely after verify()
                        trial_image = Image.open(StringIO(data))
                        trial_image.load()
                        # verify() is the only method that can spot a corrupt PNG,
                        #  but it must be called immediately after the constructor
                        trial_image = Image.open(StringIO(data))
                        trial_image.verify()
                    except Exception:
                        # if a "bad" file is found we just skip it.
                        continue
                    while 1:
                        title = ' '.join([self.title, str(count)])
                        slug = slugify(title)
                        slug = str(uuid.uuid4())
                        try:
                            p = Photo.objects.get(title_slug=slug)
                        except Photo.DoesNotExist:
                            photo = Photo(title=filename,
                                          title_slug=slug,
                                          description=self.description,
                                          is_active=False,
                                          gallery=gallery,
                                          crop_from='top'
                                          )
                            photo.image.save(randomFilename(filename), ContentFile(data))
                            count = count + 1
                            break
                        count = count + 1
            zip.close()
            return gallery





class Photo(models.Model):
    date_added = models.DateTimeField(_('date added'), default=datetime.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(_('title'), max_length=100, unique=False)
    title_slug = models.SlugField(_('slug'), unique=True, help_text=('A "slug" is a unique URL-friendly title for an object.'))
    description = models.TextField(_('description'), blank=True)
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField(_('met _keywords'), max_length=255, help_text=_('Comma-delimited set of SEO keywords for meta tag. ex: puppy, abstract, family, rainbow,...'), blank=True)
    
    gallery = models.ForeignKey(Gallery)
    image = models.ImageField(_('image'), max_length=IMAGE_FIELD_MAX_LENGTH, upload_to=PROOFING_PATH)
    date_taken = models.DateTimeField(_('date taken'), null=True, blank=True, editable=False)
    view_count = models.PositiveIntegerField(default=0, editable=False)
    crop_from = models.CharField(_('crop from'), blank=True, max_length=10, default='center', choices=CROP_ANCHOR_CHOICES)
    
    class Meta:
        ordering = ['date_added']
        get_latest_by = 'date_added'
        verbose_name = _("photo")
        verbose_name_plural = _("photos")
    
    @property
    def EXIF(self):
        try:
            return EXIF.process_file(open(self.image.path, 'rb'))
        except:
            try:
                return EXIF.process_file(open(self.image.path, 'rb'), details=False)
            except:
                return {}

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()
    
    def get_absolute_url(self):
        return reverse(PROOFING_URL_NAMES.PHOTO, args=[self.title_slug])

    def cache_path(self):
        return os.path.join(os.path.dirname(self.image.path), "cache")

    def cache_url(self):
        return '/'.join([os.path.dirname(self.image.url), "cache"])

    def image_filename(self):
        return os.path.basename(force_unicode(self.image.path))
    
    def add_accessor_methods(self, *args, **kwargs):
        for size in PhotoSizeCache().sizes.keys():
            setattr(self, 'get_%s_size' % size,
                    curry(self._get_SIZE_size, size=size))
            setattr(self, 'get_%s_photosize' % size,
                    curry(self._get_SIZE_photosize, size=size))
            setattr(self, 'get_%s_url' % size,
                    curry(self._get_SIZE_url, size=size))
            setattr(self, 'get_%s_filename' % size,
                    curry(self._get_SIZE_filename, size=size))
    
    def _get_filename_for_size(self, size):
        size = getattr(size, 'name', size)
        base, ext = os.path.splitext(self.image_filename())
        return ''.join([base, '_', size, ext])

    def _get_SIZE_photosize(self, size):
        return PhotoSizeCache().sizes.get(size)

    def _get_SIZE_size(self, size):
        photosize = PhotoSizeCache().sizes.get(size)
        if not self.size_exists(photosize):
            self.create_size(photosize)
        return Image.open(self._get_SIZE_filename(size)).size

    def _get_SIZE_url(self, size):
        photosize = PhotoSizeCache().sizes.get(size)
        if not self.size_exists(photosize):
            self.create_size(photosize)
        if photosize.increment_count:
            self.increment_count()
        return '/'.join([self.cache_url(), self._get_filename_for_size(photosize.name)])

    def _get_SIZE_filename(self, size):
        photosize = PhotoSizeCache().sizes.get(size)
        return smart_str(os.path.join(self.cache_path(),
                            self._get_filename_for_size(photosize.name)))
    def get_thumb_url(self):
        default_size = "%dx%d" %(PROOFING_DEFAULT_THUMB_SIZE)
            
        try:
            self._get_SIZE_url(default_size)
        except:
            ps = PhotoSize(
                            name = default_size,
                            width = PROOFING_DEFAULT_THUMB_SIZE[0],
                            height = PROOFING_DEFAULT_THUMB_SIZE[1],
                            quality = JPEG_QUALITY_CHOICES[3][0],
                            upscale = False,
                            crop = True,
                            pre_cache = False,
                            increment_count =  False,
                            watermark = None,
                            )
            ps.save()
            self.add_accessor_methods()

        return self._get_SIZE_url(default_size)
    
    def increment_count(self):
        self.view_count += 1
        models.Model.save(self)
        
    def size_exists(self, photosize):
        func = getattr(self, "get_%s_filename" % photosize.name, None)
        if func is not None:
            if os.path.isfile(func()):
                return True
        return False

    def resize_image(self, im, photosize):
        cur_width, cur_height = im.size
        new_width, new_height = photosize.size
        if photosize.crop:
            ratio = max(float(new_width)/cur_width,float(new_height)/cur_height)
            x = (cur_width * ratio)
            y = (cur_height * ratio)
            xd = abs(new_width - x)
            yd = abs(new_height - y)
            x_diff = int(xd / 2)
            y_diff = int(yd / 2)
            if self.crop_from == 'top':
                box = (int(x_diff), 0, int(x_diff+new_width), new_height)
            elif self.crop_from == 'left':
                box = (0, int(y_diff), new_width, int(y_diff+new_height))
            elif self.crop_from == 'bottom':
                box = (int(x_diff), int(yd), int(x_diff+new_width), int(y)) # y - yd = new_height
            elif self.crop_from == 'right':
                box = (int(xd), int(y_diff), int(x), int(y_diff+new_height)) # x - xd = new_width
            else:
                box = (int(x_diff), int(y_diff), int(x_diff+new_width), int(y_diff+new_height))
            im = im.resize((int(x), int(y)), Image.ANTIALIAS).crop(box)
        else:
            if not new_width == 0 and not new_height == 0:
                ratio = min(float(new_width)/cur_width,
                            float(new_height)/cur_height)
            else:
                if new_width == 0:
                    ratio = float(new_height)/cur_height
                else:
                    ratio = float(new_width)/cur_width
            new_dimensions = (int(round(cur_width*ratio)),
                              int(round(cur_height*ratio)))
            if new_dimensions[0] > cur_width or \
               new_dimensions[1] > cur_height:
                if not photosize.upscale:
                    return im
            im = im.resize(new_dimensions, Image.ANTIALIAS)
        return im

    def create_size(self, photosize):
        if self.size_exists(photosize):
            return
        if not os.path.isdir(self.cache_path()):
            os.makedirs(self.cache_path())
        try:
            im = Image.open(self.image.path)
        except IOError:
            return
        # Save the original format
        im_format = im.format
        # Apply effect if found
#        if self.effect is not None:
#            im = self.effect.pre_process(im)
#        elif photosize.effect is not None:
#            im = photosize.effect.pre_process(im)
        # Resize/crop image
        if im.size != photosize.size and photosize.size != (0, 0):
            im = self.resize_image(im, photosize)
        # Apply watermark if found
        if photosize.watermark is not None:
            im = photosize.watermark.post_process(im)
        # Save file
        im_filename = getattr(self, "get_%s_filename" % photosize.name)()
        
        #im.save(im_filename)
        print self.image.path
        im.save(im_filename, 'JPEG', quality=int(photosize.quality), optimize=True)
            
            
        try:
            if im_format != 'JPEG':
                try:
                    im.save(im_filename)
                    return
                except KeyError:
                    pass
            im.save(im_filename, 'JPEG', quality=int(photosize.quality), optimize=True)
        except IOError, e:
            if os.path.isfile(im_filename):
                os.unlink(im_filename)
            raise e

    def remove_size(self, photosize, remove_dirs=True):
        if not self.size_exists(photosize):
            return
        filename = getattr(self, "get_%s_filename" % photosize.name)()
        if os.path.isfile(filename):
            os.remove(filename)
        if remove_dirs:
            self.remove_cache_dirs()
            
    def clear_cache(self):
        cache = PhotoSizeCache()
        for photosize in cache.sizes.values():
            self.remove_size(photosize, False)
        self.remove_cache_dirs()

    def pre_cache(self):
        cache = PhotoSizeCache()
        for photosize in cache.sizes.values():
            if photosize.pre_cache:
                self.create_size(photosize)

    def remove_cache_dirs(self):
        try:
            os.removedirs(self.cache_path())
        except:
            pass
        
    def save(self, *args, **kwargs):
        if self.title_slug is None:
            self.title_slug = slugify(self.title)
            
        if self.date_taken is None:
            try:
                exif_date = self.EXIF.get('EXIF DateTimeOriginal', None)
                if exif_date is not None:
                    d, t = str.split(exif_date.values)
                    year, month, day = d.split(':')
                    hour, minute, second = t.split(':')
                    self.date_taken = datetime(int(year), int(month), int(day),
                                               int(hour), int(minute), int(second))
            except:
                pass
        if self.date_taken is None:
            self.date_taken = datetime.now()
        if self._get_pk_val():
            self.clear_cache()
        super(Photo, self).save(*args, **kwargs)
        self.pre_cache()

    def delete(self):
        assert self._get_pk_val() is not None, "%s object can't be deleted because its %s attribute is set to None." % (self._meta.object_name, self._meta.pk.attname)
        self.clear_cache()
        super(models.Model, self).delete()
    
class Watermark(models.Model):
    image = models.ImageField(_('image'), upload_to=os.path.join(PROOFING_PATH, 'watermarks'))
    style = models.CharField(_('style'), max_length=5, choices=WATERMARK_STYLE_CHOICES, default='scale')
    opacity = models.FloatField(_('opacity'), default=1, help_text=_("The opacity of the overlay."))

    class Meta:
        verbose_name = _('watermark')
        verbose_name_plural = _('watermarks')

    def post_process(self, im):
        mark = Image.open(self.image.path)
        return apply_watermark(im, mark, self.style, self.opacity)
    
    
    
class PhotoSize(models.Model):
    name = models.CharField(_('name'), max_length=20, unique=True, help_text=_('Photo size name should contain only letters, numbers and underscores. Examples: "thumbnail", "display", "small", "main_page_widget".'))
    width = models.PositiveIntegerField(_('width'), default=0, help_text=_('If width is set to "0" the image will be scaled to the supplied height.'))
    height = models.PositiveIntegerField(_('height'), default=0, help_text=_('If height is set to "0" the image will be scaled to the supplied width'))
    quality = models.PositiveIntegerField(_('quality'), choices=JPEG_QUALITY_CHOICES, default=70, help_text=_('JPEG image quality.'))
    upscale = models.BooleanField(_('upscale images?'), default=False, help_text=_('If selected the image will be scaled up if necessary to fit the supplied dimensions. Cropped sizes will be upscaled regardless of this setting.'))
    crop = models.BooleanField(_('crop to fit?'), default=False, help_text=_('If selected the image will be scaled and cropped to fit the supplied dimensions.'))
    pre_cache = models.BooleanField(_('pre-cache?'), default=False, help_text=_('If selected this photo size will be pre-cached as photos are added.'))
    increment_count = models.BooleanField(_('increment view count?'), default=False, help_text=_('If selected the image\'s "view_count" will be incremented when this photo size is displayed.'))
    watermark = models.ForeignKey('Watermark', null=True, blank=True, related_name='photo_sizes', verbose_name=_('watermark image'))

    class Meta:
        ordering = ['width', 'height']
        verbose_name = _('photo size')
        verbose_name_plural = _('photo sizes')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    def clear_cache(self):
        for cls in Photo.__subclasses__():
            for obj in cls.objects.all():
                obj.remove_size(self)
                if self.pre_cache:
                    obj.create_size(self)
        PhotoSizeCache().reset()

    def save(self, *args, **kwargs):
        if self.crop is True:
            if self.width == 0 or self.height == 0:
                raise ValueError("PhotoSize width and/or height can not be zero if crop=True.")
        super(PhotoSize, self).save(*args, **kwargs)
        PhotoSizeCache().reset()
        self.clear_cache()

    def delete(self):
        assert self._get_pk_val() is not None, "%s object can't be deleted because its %s attribute is set to None." % (self._meta.object_name, self._meta.pk.attname)
        self.clear_cache()
        super(PhotoSize, self).delete()

    def _get_size(self):
        return (self.width, self.height)
    def _set_size(self, value):
        self.width, self.height = value
    size = property(_get_size, _set_size)
    
        
        
        
        
        
class PhotoSizeCache(object):
    __state = {"sizes": {}}

    def __init__(self):
        self.__dict__ = self.__state
        if not len(self.sizes):
            sizes = PhotoSize.objects.all()
            for size in sizes:
                self.sizes[size.name] = size

    def reset(self):
        self.sizes = {}


# Set up the accessor methods
def add_methods(sender, instance, signal, *args, **kwargs):
    """ Adds methods to access sized images (urls, paths)

    after the Photo model's __init__ function completes,
    this method calls "add_accessor_methods" on each instance.
    """
    if hasattr(instance, 'add_accessor_methods'):
        instance.add_accessor_methods()

# connect the add_accessor_methods function to the post_init signal
post_init.connect(add_methods)     
        
        
        
