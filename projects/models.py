from django.conf import settings
from django.db import models


class Project(models.Model):

    TYPES = [
    ('BACKEND', 'BACKEND'),
    ('FRONTEND', 'FRONTEND'),
    ('iOS', 'iOS'),
    ('ANDROID', 'ANDROID')
    ]

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    type = models.CharField(choices=TYPES, max_length=8)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Contributor(models.Model):

    ROLES = [
    ('AUTHOR', 'AUTHOR'),
    ('CONTRIBUTOR', 'CONTRIBUTOR')
    ]

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='contributors')
    role = models.CharField(max_length=12, choices=ROLES, default='CONTRIBUTOR')

    class Meta:
        unique_together = ('project', 'user')


class Issue(models.Model):

    TAGS = [
    ('BUG', 'BUG'),
    ('TASK', 'TASK'),
    ('UPGRADE', 'UPGRADE')
    ]

    PRIORITIES = [
        ('LOW', 'LOW'),
        ('MEDIUM', 'MEDIUM'),
        ('HIGH', 'HIGH')
    ]

    STATUSES = [
        ('TODO', 'TODO'),
        ('IN PROGRESS', 'IN PROGRESS'),
        ('DONE', 'DONE')
    ]

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    tag = models.CharField(choices=TAGS, max_length=7)
    priority = models.CharField(choices=PRIORITIES, max_length=12, default='LOW')
    status = models.CharField(choices=STATUSES, max_length=12, default='TODO')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issue_author')
    assignee = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=author)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.TextField(max_length=2048)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)