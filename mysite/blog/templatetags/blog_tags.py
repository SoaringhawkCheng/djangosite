# -*- coding: utf-8 -*-

import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from mysite.blog.models import Post

register = template.Library()


# 处理数据并返回一个字符串
@register.simple_tag
def total_posts():
    # return Post.objects.filter(status='published').count()
    return Post.published.count()


# 处理数据并返回一个渲染过的模板
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# 处理数据并在上下文中设置一个变量
@register.assignment_tag
def get_most_commented_posts(count=5):
    # annotate聚合查询，Count是聚合函数
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


# 注册了一个过滤器
@register.filter(name='markdown')
def markdown_format(text):
    # 可以在blog中使用markdown语法
    return mark_safe(markdown.markdown(text))
