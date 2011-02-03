
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings

from models import Category, Gallery, Photo
from decorators import check_perm_for
from utils.breadcrumb import WBBreadcrumbTrail, WBBreadcrumb

def index(request, template_name="proofing/generic_list.html"):
    objects = Category.active.all()
    
    breadcrumbtrail = WBBreadcrumbTrail(WBBreadcrumb('Home',reverse('proofing-index')))
    page_title = 'Show Index'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def show_category(request, slug, template_name="proofing/generic_list.html"):
    current = get_object_or_404(Category, slug = slug)
    
    objects = Gallery.active.filter(category=current)
    
    breadcrumbtrail = WBBreadcrumbTrail(WBBreadcrumb('Home',reverse('proofing-index')),current)
    page_title = 'Show Category'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@check_perm_for(Gallery)
def show_gallery(request, obj, template_name="proofing/generic_list.html"):
    #current = get_object_or_404(Gallery, slug = gallery_slug)
    current = obj
    parent = current.category
    
    objects = Photo.objects.filter(gallery=current)
    
    breadcrumbtrail = WBBreadcrumbTrail(WBBreadcrumb('Home',reverse('proofing-index')),parent, current)
    page_title = 'Show Gallery'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@check_perm_for(Photo)
def show_photo(request, obj, template_name="proofing/photo.html"):
    photo = photo
    
    breadcrumbtrail = WBBreadcrumbTrail(
                                        WBBreadcrumb('Home',reverse('proofing-index')),
                                        photo.gallery.category, 
                                        photo.gallery,
                                        photo)
    page_title = 'Show Photo'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


