from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('words.views',
    url(r'^$', 'word_list'),
    url(r'^favorites', 'favorites'),
    url(r'^xml', 'xml'),
    url(r'^api/get_word_ids', 'get_word_ids'),
    url(r'api/get_favorites_ids', 'get_favorites_ids'),
    url(r'api/get_word/(?P<id>\d+)', 'get_word'),
    url(r'api/add_word', 'add_word'),
    url(r'api/edit_word', 'edit_word'),
    url(r'api/delete_word', 'delete_word'),
    url(r'api/add_to_fav', 'add_to_fav'),
    url(r'api/remove_fav', 'remove_fav'),
)
