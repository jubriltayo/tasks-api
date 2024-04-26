from django.urls import path

from . import views

urlpatterns = [
    path('', views.TaskListCreateView.as_view()),
    path('uncompleted/', views.TaskUncompletedView.as_view()),
    path('<int:pk>/', views.TaskDetailView.as_view()),
    path('<int:pk>/update/', views.TaskUpdateView.as_view()),
    path('<int:pk>/delete/', views.TaskDestroyView.as_view()),
]
