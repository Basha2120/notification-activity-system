from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Notification
from posts.models import Post
from accounts.models import Follow
from .serializers import NotificationSerializer, UnreadCountSerializer

User = get_user_model()

class NotificationPagination(PageNumberPagination):
    page_size = 20

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_count(request):
    """API view to return unread notification count."""
    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return Response({'count': count})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_read(request, pk):
    """Mark a single notification as read."""
    try:
        n = Notification.objects.get(pk=pk, recipient=request.user)
        n.is_read = True
        n.save(update_fields=['is_read'])
        return Response({'status': 'read'})
    except Notification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_read(request):
    """Mark all unread notifications as read."""
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return Response({'status': 'all_read'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_list(request):
    """API view to list all notifications for the user."""
    qs = Notification.objects.filter(recipient=request.user).select_related('actor', 'notification_type').order_by('-created_at')
    paginator = NotificationPagination()
    page = paginator.paginate_queryset(qs, request)
    serializer = NotificationSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed_api(request):
    """API view for the activity feed."""
    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    posts = Post.objects.filter(author_id__in=following_ids).select_related('author').order_by('-created_at')
    paginator = NotificationPagination()
    page = paginator.paginate_queryset(posts, request)
    # We'd need a PostSerializer for a full API, but for now we confirm the logic
    return Response({'posts_count': posts.count()})

@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def follow_api(request, username):
    """API view for follow/unfollow."""
    target = get_object_or_404(User, username=username)
    if request.method == 'POST':
        if target != request.user:
            Follow.objects.get_or_create(follower=request.user, following=target)
            return Response({'status': 'followed'})
    elif request.method == 'DELETE':
        Follow.objects.filter(follower=request.user, following=target).delete()
        return Response({'status': 'unfollowed'})
    return Response(status=status.HTTP_400_BAD_REQUEST)
