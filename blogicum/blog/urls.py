from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'blog'

urlpatterns = [
                  path('',
                       views.PostIndexListView.as_view(), name='index'),
                  path('posts/<int:post_id>/',
                       views.PostDetailView.as_view(), name='post_detail'),
                  path('category/<slug:category_slug>/',
                       views.PostCategoryListView.as_view(),
                       name='category_posts'),

                  path('post/create/',
                       views.PostCreateView.as_view(), name='post_create'),
                  path('post/<int:post_id>/edit/',
                       views.PostUpdateView.as_view(), name='post_edit'),
                  path('post/<int:post_id>/delete/',
                       views.PostDeleteView.as_view(), name='post_delete'),

                  path('profile/<str:username>/',
                       views.ProfileListView.as_view(),
                       name='profile'),
                  path('edit_profile/',
                       views.ProfileUpdateView.as_view(),
                       name='edit_profile'),

                  path('posts/<int:post_id>/comment/',
                       views.CommentCreateView.as_view(),
                       name='comment_create'),
                  path('comment/<int:post_id>/edit_comment/<int:comment_id>/',
                       views.CommentUpdateView.as_view(),
                       name='comment_edit'),
                  path('comment/<int:post_id>/delete_comment/<int:comment_id>/',
                       views.CommentDeleteView.as_view(),
                       name='comment_delete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
