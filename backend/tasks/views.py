from django.shortcuts import render
from rest_framework import authentication, generics, permissions

from .models import Task
from .serializers import TaskSerializer
from api.authentication import TokenAuthentication
from api.mixins import UserPermissionMixin, UserQueryMixin


class TaskListCreateView(UserQueryMixin, UserPermissionMixin, generics.ListCreateAPIView): # UserPermissionMixin,
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)

class TaskUncompletedView(UserQueryMixin, UserPermissionMixin, generics.ListAPIView):
    # queryset = Task.objects.filter(completed=False)
    queryset = Task.objects.uncompleted()
    serializer_class = TaskSerializer
    

class TaskDetailView(UserQueryMixin, UserPermissionMixin, generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskUpdateView(UserQueryMixin, UserPermissionMixin, generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
        serializer.save()

class TaskDestroyView(UserQueryMixin, UserPermissionMixin, generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_destroy(self, instance):
        super().perform_destroy(instance)