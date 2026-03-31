from django.contrib import admin
from django.urls import path, include

from posts import template_views as posts_views
from notifications import views as notifications_views

urlpatterns = [
    path('', posts_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('notifications/', include('notifications.urls')),
    path('api/notifications/', include('notifications.api_urls')),
    path('api/feed/', notifications_views.feed_api, name='api-feed'),
    path('api/follow/<str:username>/', notifications_views.follow_api, name='api-follow'),
    path('', include('posts.urls')),
]
