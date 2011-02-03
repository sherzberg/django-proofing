
from django.shortcuts import get_object_or_404
from django.http import Http404

from models import *


# this could be better
def check_perm_for(cls):
    
    def _wrap(function):
        def _inner(request,**kwargs):
            
            slug = kwargs['slug']
            object = get_object_or_404(cls, slug = slug)
            user = request.user
            
            has_perm = object.is_users(user)
            kwargs.pop('slug')
            
            if has_perm:
                return function(request, object, **kwargs)
            else:
                raise Http404
            
        return _inner
    
    return _wrap

