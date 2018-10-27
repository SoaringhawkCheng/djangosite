# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
# from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.

class PublishedManager(models.Manager):
    # 自动生成查询集
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts')  # 反向关联名
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)  # 创建时自动保存当前日期
    updated = models.DateTimeField(auto_now=True)  # 更新保存时自动更新当前日期
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    published = PublishedManager()  # 自定义属性，用于生成查询集，定义派生的属性必须定义默认属性
    objects = models.Manager() # 默认的Post.objects.filter等就是由model.Manager生成的属性，调用get_queryset生辰查询集合
    tags = TaggableManager()

    class Meta:
        # 查询数据库的时候默认返回的是根据publish字段进行降序排列过的结果
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year, self.publish.strftime('%m'), self.publish.strftime('%d'), self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
