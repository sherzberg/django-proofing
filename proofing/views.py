
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings

from models import Category, Gallery, Photo

def index(request, template_name="proofing/generic_list.html"):
    objects = Category.active.all()
        
    page_title = 'Show Index'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def show_category(request, category_slug, template_name="proofing/generic_list.html"):
    current = get_object_or_404(Category, slug = category_slug)
    
    objects = Gallery.active.filter(category=current)
    
    page_title = 'Show Category'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def show_gallery(request, gallery_slug, template_name="proofing/generic_list.html"):
    current = get_object_or_404(Gallery, slug = gallery_slug)
    parent = current.category
    
    objects = Photo.objects.filter(gallery=current)
    
    page_title = 'Show Gallery'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def show_photo(request, photo_slug, template_name="proofing/photo.html"):
    photo = get_object_or_404(Photo, slug = photo_slug)
         
    page_title = 'Show Photo'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


