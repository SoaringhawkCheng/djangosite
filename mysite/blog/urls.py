from django.conf.urls import url
from mysite.blog import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    # post由单词和连字符组成, 可以使用url的name,reverse得到url
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', views.post_detail, name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
]
