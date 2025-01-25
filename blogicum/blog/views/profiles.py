from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

from django.views.generic import (
    ListView, UpdateView
)
from ..models import Post
from ..forms import ProfileEditForm

User = get_user_model()


class ProfileListView(ListView):
    """Отправляет список постов для данного пользователя."""

    model = Post
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get_queryset(self):
        filters = {'author__username': self.kwargs['username']}
        if self.request.user.username != self.kwargs['username']:
            filters.update(
                {
                    'is_published__exact': True,
                    'pub_date__lte': timezone.now()
                }
            )
            return (self.model.objects.select_related('author')
                    .filter(**filters).order_by('-pub_date')
                    .annotate(comment_count=Count('comments')))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context


class ProfileUpdateView(UpdateView):
    """Показать форму редактирования для данного пользователя."""

    template_name = 'blog/profile_edit.html'
    form_class = ProfileEditForm

    def get_object(self, queryset=None):
        """Вернуть объект пользователя."""
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user])
