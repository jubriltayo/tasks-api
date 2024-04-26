from django.db import models
from django.utils import timezone
from django.conf import settings

User = settings.AUTH_USER_MODEL


class TaskQuerySet(models.QuerySet):
    def is_completed(self):
        return self.filter(completed=True)


class TaskManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return TaskQuerySet(self.model, self._db)


class Task(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)

    objects = TaskManager()



