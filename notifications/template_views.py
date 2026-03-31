from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notification

@login_required
def notification_page(request):
    """View to list all notifications for a user."""
    notifications = (
        Notification.objects
        .filter(recipient=request.user)
        .select_related('actor', 'notification_type')
        .order_by('-created_at')[:50]
    )
    # Mark as read if user views the page? 
    # Actually, we might want a separate "mark all read" action.
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications,
    })
