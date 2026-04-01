from django.urls import path
from . import template_views

urlpatterns = [
    path('', template_views.notification_page, name='notifications'),
    path('<int:pk>/go/', template_views.notification_redirect, name='notification-redirect'),
]
