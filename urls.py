from django.contrib import admin
from django.urls import path, include

from posts import template_views as posts_views

urlpatterns = [
    path('', posts_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('posts.urls')),
]
