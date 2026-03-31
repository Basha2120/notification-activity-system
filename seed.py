import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from notifications.models import NotificationType

types = [
    {'code': 'COMMENT_ADDED', 'template': '{actor} commented on your post "{target}"', 'icon': 'comment', 'colour': '#3ecf8e'},
    {'code': 'USER_FOLLOWED', 'template': '{actor} started following you', 'icon': 'follow', 'colour': '#6366f1'},
    {'code': 'MENTION', 'template': '{actor} mentioned you in a comment', 'icon': 'mention', 'colour': '#f59e0b'},
]

for t in types:
    NotificationType.objects.get_or_create(code=t['code'], defaults=t)
    print(f"Seeded {t['code']}")
