from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Count
from django.urls import reverse

from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Post, Category
from ..forms import PostForm, CommentForm


class PostMixin:
    model = Post


class PostEditMixin:
    template_name = 'blog/create.html'


class PostIndexListView(PostMixin, ListView):
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(
            pub_date__lte=timezone.now(),
            is_published__exact=True,
            category__is_published__exact=True
        ).order_by('-pub_date').annotate(comment_count=Count('comments'))


class PostCategoryListView(PostMixin, ListView):
    template_name = 'blog/category.html'
    paginate_by = 10
    _category = None

    def get_category(self):
        if not self._category:
            self._category = get_object_or_404(
                Category,
                slug=self.kwargs['category_slug'],
                is_published=True,
            )
        return self._category

    def get_queryset(self):
        category = self.get_category()
        return self.model.objects.filter(
            category__exact=category,
            is_published__exact=True,
            pub_date__lte=timezone.now()
        ).order_by('-pub_date').annotate(comment_count=Count('comments'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/detail.html'

    def get_object(self, **kwargs):
        post = get_object_or_404(
            self.model.objects.filter(pk=self.kwargs['post_id'])
        )
        if post.author == self.request.user:
            return post
        else:
            return get_object_or_404(
                self.model.objects.filter(
                    pub_date__lte=timezone.now(),
                    is_published__exact=True,
                    category__is_published__exact=True
                ),
                pk=self.kwargs['post_id']
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class PostCreateView(PostMixin, PostEditMixin, LoginRequiredMixin, CreateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user])


class PostUpdateView(PostMixin, PostEditMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm

    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(PostMixin, PostEditMixin, LoginRequiredMixin, DeleteView):
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user])
