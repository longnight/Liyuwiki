from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from wikidict import views, api
from wikidict.models import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

try:
    import private_settings2
except:
    pass

admin.autodiscover()

widget_dict = {
    'model': Definitions,
    'template_object_name': 'definitions',
    'allow_xmlhttprequest': True,
}

urlpatterns = patterns('',
    # Examples:
    url(r'^search/', include('haystack.urls')),
    url(r'random/$', views.randomview, name='random'),
    url(r'add_search_term/(?P<search_term>.+)/$', views.add_search_term, name='add_search_term'),
    url(r'add_term.html$', views.add_term, name='add_term'),
    url(r'(?P<term_uid>[\d]+)_add_def.html$', views.add_def, name='add_def'),
    url(r'(?P<term_uid>\d{6})/(?P<def_uid>\d{6})/action=add_vote', views.add_vote, name='add_vote'),
    url(r'(?P<term_uid>\d{6})/(?P<def_uid>\d{6})/action=sub_vote', views.sub_vote, name='sub_vote'),
    url(r'(?P<t_uid>\d{6})/(?P<d_uid>\d{6}).html', views.detail_single, name='detail_single'),
    url(r'(?P<term_uid>\d{6}).html', views.detail, name='detail'),    
    url(r'^about.html$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^thanks.html$', TemplateView.as_view(template_name='thanks.html'), name='thanks'),
    url(r'^technologies.html$', RedirectView.as_view(url='/support.html', permanent=True), name='technologies'),
    url(r'^support.html$', TemplateView.as_view(template_name='support.html'), name='support'),
    url(r'^ugc_guide.html$', TemplateView.as_view(template_name='ugc_guide.html'), name='ugc_guide'),
    url(r'^api.html$', TemplateView.as_view(template_name='api.html'), name='api_html'),
    url(r'^api/$', api.api, name='api_'),
    url(r'^api/v1/$', api.api, name='api'),
    url(r'^api/v1/term/(?P<term_uid>\d{6})/$', api.api_term, name='api_term'),
    url(r'^$', views.index, name='index'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

if private_settings2.admin_urls:
    urlpatterns += private_settings2.admin_urls