from django.urls import path
from . import template_views

urlpatterns = [
    path('posts/', template_views.post_list, name='post-list'),
    path('posts/new/', template_views.create_post, name='create-post'),
    path('posts/<int:pk>/', template_views.post_detail, name='post-detail'),
]
