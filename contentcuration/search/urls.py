from django.conf.urls import url
import search.views as views
from haystack.views import SearchView

urlpatterns = [
    url(r'^$', SearchView(), name='haystack_search'),
    url(r'^items/$', views.search_items),
    url(r'^topics/$', views.search_topics)
]
