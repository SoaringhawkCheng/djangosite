# -*- coding: utf-8 -*-

from django import template

from mysite.blog.models import Post

register = template.Library()


# 处理数据并返回一个字符串
@register.simple_tag
def total_posts():
    # return Post.objects.filter(status='published').count()
    return Post.published.count()


# 处理数据并返回一个渲染过的模板
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=2):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}
