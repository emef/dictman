from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('words.views',
    url(r'^$', 'word_list'),
    url(r'^api/get_word_ids', 'get_word_ids'),
    url(r'api/get_word/(?P<id>\d+)', 'get_word'),
)
