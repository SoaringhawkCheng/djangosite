# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from haystack.query import SearchQuerySet
from taggit.models import Tag

from mysite.blog.forms import EmailPostForm, CommentForm, SearchForm
from mysite.blog.models import Post
from mysite.settings import EMAIL_HOST_USER


# Create your views here.

def post_list(request, tag_slug=None):
    obj_list = Post.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        obj_list = obj_list.filter(tags__in=[tag])

    paginator = Paginator(obj_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html',
                  context={'posts': posts, 'page': page, 'tag': tag, 'tag_slug': tag_slug})


def post_detail(request, year: str, month: int, day: int, slug) -> None:
    post = get_object_or_404(Post, slug=slug, status='published', publish__year=int(year), publish__month=int(month),
                             publish__day=int(day))
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)  # 保存不提交
            new_comment.post = post
            new_comment.save()

    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html',
                  context={'post': post, 'comments': comments, 'new_comment': new_comment,
                           'comment_form': comment_form})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)  # 保存提交的表单
        if form.is_valid():
            cd = form.cleaned_data  # 获取验证过的数据，是个dict
            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['email'])
            send_mail(subject, message, EMAIL_HOST_USER, [cd['to']])
            sent = True

    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', context={'post': post, 'form': form, 'sent': sent})


def post_search(request):
    form = SearchForm()
    cd = results = total_results = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post).filter(content=cd["query"]).load_all()
            total_results = results.count()

    return render(request, 'blog/post/search.html',
                  {'form': form, 'cd': cd, 'results': results, 'total_results': total_results})
