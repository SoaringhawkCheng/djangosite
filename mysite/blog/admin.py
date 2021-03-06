# -*- coding: utf-8 -*-
from django.contrib import admin
from mysite.blog.models import Post, Comment


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')  # 列表显示字段
    list_filter = ('status', 'created', 'publish', 'author')  # 过滤
    search_fields = ('title', 'body')  # 搜索
    prepopulated_fields = {'slug': ('title',)}  # 预填充字段
    raw_id_fields = ('author',)  # 显示外键的详细信息
    date_hierarchy = 'publish'  # 基于时间的快速导航栏
    ordering = ['status', 'publish']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)