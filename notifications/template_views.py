from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Notification
from posts.models import Post, Comment

@login_required
def notification_page(request):
    """View to list all notifications for a user."""
    notifications = (
        Notification.objects.filter(recipient=request.user)
        .select_related('actor', 'notification_type')
        .order_by('-created_at')[:50]
    )
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})

@login_required
def notification_redirect(request, pk):
    """Marks a notification as read and redirects to its target."""
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save(update_fields=['is_read'])
    
    target = notification.target
    if not target:
        return redirect('notifications')
    
    # Redirection logic based on target type
    if isinstance(target, Post):
        return redirect('post-detail', pk=target.pk)
    elif isinstance(target, Comment):
        return redirect('post-detail', pk=target.post.pk)
    elif hasattr(target, 'username'): # Maybe a User profile?
        return redirect('/accounts/profile/' + target.username + '/')
        
    return redirect('notifications')
