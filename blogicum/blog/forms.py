from django import forms
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileEditForm(forms.ModelForm):
    """Форма редактирования профиля пользователя."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class PostForm(forms.ModelForm):
    """Форма создания поста."""

    class Meta:
        model = Post
        exclude = ('created_at', 'is_published', 'author')
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'}
            ),
        }


class CommentForm(forms.Form):
    """Форма создания комментария."""

    class Meta:
        model = Comment
        fields = ('text',)
