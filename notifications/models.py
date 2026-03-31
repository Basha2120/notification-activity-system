from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class NotificationType(models.Model):
    code = models.CharField(max_length=50, unique=True)
    template = models.CharField(max_length=255)
    icon = models.CharField(max_length=50, default='bell')
    colour = models.CharField(max_length=7, default='#6366f1')

    def __str__(self):
        return self.code

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', null=True)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    target_object_id = models.PositiveIntegerField(null=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

def create_notification(recipient, actor, notification_type_code, verb, target=None):
    if recipient == actor: return None
    nt = NotificationType.objects.get(code=notification_type_code)
    kwargs = {'recipient': recipient, 'actor': actor, 'notification_type': nt, 'verb': verb}
    if target:
        kwargs['target_content_type'] = ContentType.objects.get_for_model(target)
        kwargs['target_object_id'] = target.pk
    return Notification.objects.create(**kwargs)
