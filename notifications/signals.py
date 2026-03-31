import re
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender='posts.Comment')
def notify_on_comment(sender, instance, created, **kwargs):
    if not created: return
    from notifications.models import create_notification
    post = instance.post
    if instance.author != post.author:
        create_notification(
            recipient=post.author, actor=instance.author,
            notification_type_code='COMMENT_ADDED',
            verb=f'commented on your post "{post.title}"', target=post
        )
    _notify_mentions(instance)

@receiver(post_save, sender='accounts.Follow')
def notify_on_follow(sender, instance, created, **kwargs):
    if not created: return
    from notifications.models import create_notification
    create_notification(
        recipient=instance.following, actor=instance.follower,
        notification_type_code='USER_FOLLOWED',
        verb='started following you', target=instance.following
    )

def _notify_mentions(comment):
    from notifications.models import create_notification
    MENTION_RE = re.compile(r'(?<!\w)@([\w.@+-]+)', re.UNICODE)
    usernames = set(MENTION_RE.findall(comment.body))
    mentioned_users = User.objects.filter(username__in=usernames)
    for user in mentioned_users:
        if user != comment.author:
            create_notification(
                recipient=user, actor=comment.author,
                notification_type_code='MENTION',
                verb='mentioned you in a comment', target=comment
            )
