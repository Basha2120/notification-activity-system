from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Notification, NotificationType

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class NotificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationType
        fields = ['id', 'code', 'icon', 'colour']

class NotificationSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(read_only=True)
    notification_type = NotificationTypeSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'notification_type', 'verb', 'is_read', 'created_at']

class UnreadCountSerializer(serializers.Serializer):
    count = serializers.IntegerField()
