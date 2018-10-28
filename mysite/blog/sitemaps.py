# -*- coding: utf-8 -*-

from django.contrib.sitemaps import Sitemap

from mysite.blog.models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    # 返回站点地图中包含对象的查询集
    def items(self):
        return Post.published.all()

    # 接受item返回的对象并返回对象的最后修改日期
    def lastmod(self, obj):
        return obj.publish
