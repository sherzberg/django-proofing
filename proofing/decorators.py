
from django.shortcuts import get_object_or_404
from django.http import Http404

from models import *

'''
This decorator is to check object permissions based on the rules defined for Gallery and Photo models (
or really an model object that implements a is_users(user) method. The nice thing about this method is that
instead of passing a string slug to a view, the actual object is passed (if the tests are passed and an
object was found with get_object_or_404.
'''

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

