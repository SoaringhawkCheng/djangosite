# -*- coding: utf-8 -*-

from haystack import indexes
from mysite.blog.models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    publish = indexes.DateTimeField