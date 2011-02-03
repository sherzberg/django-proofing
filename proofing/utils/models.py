from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _


class WBManager(models.Manager):
    def get_query_set(self):
        objects = super(WBManager, self).get_query_set()
        objects.filter(is_active=True)
        return objects.distinct()
    
class WBModel(models.Model):
    
    date_added = models.DateTimeField(_('date added'), auto_now_add=True, editable=False)
    date_changed = models.DateTimeField(_('date changed'), auto_now_add=True, auto_now=True)

    slug = models.SlugField(_('slug'), unique=True, help_text=_('A "slug" is a unique URL-friendly title for an object'))
    description = models.TextField(_('description'), blank=True)
    
    is_active = models.BooleanField(default=True)
    
    meta_keywords = models.CharField(_('meta keywords'), max_length=255, help_text=_('Comma-delimited set of SEO keywords for meta tag. ex: ifa,var,varsity,fb,football,...'), blank=True)
    
    class Meta:
        abstract = True
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        
    objects = models.Manager()
    active = WBManager()
    
    def __unicode__(self):
        return self.title
    
    def __str__(self):
        return self.__unicode__()
    
    def save(self, *args, **kwargs):
        self.date_changed = datetime.now()
        super(WBModel, self).save(*args, **kwargs)
            
            