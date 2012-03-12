import os
from django.conf.urls.defaults import *
from Allthink.views import *

site_media = os.path.join(
    os.path.dirname(__file__), 'site_media'
)

media = os.path.join(
    os.path.dirname(__file__), 'media'
)

urlpatterns = patterns('',

    # Browsing
    (r'^$', main_page),
    (r'^user/(\w+)/$', user_page),
    (r'^user/(\w+)/lesson/create/$', create_lesson),
    (r'^user/(\w+)/$', user_page),

    # Session management
    (r'^login/$', login),
    (r'^logout/$', logout_page),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
         { 'document_root': site_media }),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': media}),
    (r'^signup/$', register_page),
    (r'^signup/teacher/$', teacher_register_page),
)
