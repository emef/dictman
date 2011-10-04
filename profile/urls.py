from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'profile/login.djhtml'}),
    url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^register', 'profile.views.register'),
)
