from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='api-notifications'),
    path('unread-count/', views.unread_count, name='unread-count'),
    path('<int:pk>/read/', views.mark_read, name='mark-read'),
    path('read-all/', views.mark_all_read, name='mark-all-read'),
    path('feed/', views.feed_api, name='api-feed'),
    path('follow/<str:username>/', views.follow_api, name='api-follow'),
]
