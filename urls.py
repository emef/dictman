from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

#enable admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'dictman.views.home', name='home'),
    # url(r'^dictman/', include('dictman.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
