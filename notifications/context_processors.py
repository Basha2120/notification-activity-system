from .models import Notification

def unread_notifications(request):
    """Context processor for unread notification count and list."""
    if not request.user.is_authenticated:
        return {'unread_count': 0, 'latest_notifications': []}

    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    latest = (
        Notification.objects
        .filter(recipient=request.user)
        .select_related('actor', 'notification_type')
        .order_by('-created_at')[:5]
    )
    return {'unread_count': unread_count, 'latest_notifications': latest}
