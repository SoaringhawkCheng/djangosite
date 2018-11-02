# -*- coding: utf-8 -*-

from django.conf.urls import url
from bookmarks.account.views import user_login

urlpatterns = [
    url(r'^login/$', user_login, name='login')
]