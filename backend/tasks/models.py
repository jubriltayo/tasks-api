from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models import Q

User = settings.AUTH_USER_MODEL


class TaskQuerySet(models.QuerySet):
    def is_completed(self):
        return self.filter(completed=True)
    
    def uncompleted(self):
        return self.filter(completed=False)

    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs = self.filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs


class TaskManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return TaskQuerySet(self.model, self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)

    def uncompleted(self):
        return self.get_queryset().uncompleted()


class Task(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)

    objects = TaskManager()



