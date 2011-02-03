
from django.template import Template, Context

trail_template = Template('''
<ul class="{{ul_class}}">
{% for item in items %}
    {% if forloop.last %}
    <li class="{{li_class}}">{{item.title}}</li>
    {% else %}
    <li class="{{li_class}}"><a href="{{item.get_absolute_url}}" alt="{{item.title}}">{{item.title}}</a></li>
    {% endif %}
{% endfor %}
</ul>
''')




class WBBreadcrumbTrail(object):
    
    def __init__(self,*args):
        self.objects = args

    def as_ul(self, ul_class='wb-breadcrumb', li_class='wb-breadcrumb-item'):
        c = Context({
                     'ul_class': ul_class,
                     'li_class': li_class,
                     'items': self.objects
                     })
        return trail_template.render(c)
        
class WBBreadcrumb(object):

    def __init__(self, title, link=None, alt=''):
        self.title = str(title)
        self.url = link
        self.alt = alt
        
    def get_title(self):
        return self.title
    
    def get_href(self):
        return ' href="%s" ' %(str(self.url)) if self.url else ''
    
    def get_absolute_url(self):
        return self.url
    
    def get_alt(self):
        return ' alt="%s" ' %(str(self.alt)) if self.alt else ''

