# -*- coding: utf-8 -*-
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from post import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^post/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from mysite.blog.sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap
}

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls', namespace='blog', app_name='blog')),  # TODO:namespace app_name
    # app_name, 应用命名空间, 表示正在部署的应用的名称
    # namespace, 表示应用的一个特定的实例
    url(r'^sitemap.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemapurl')
]
