from django.urls import path
from .views import TaskAPIView, TodoAPIView, BulkTodoAPIView

urlpatterns = [
    path('todo-nested/', TodoAPIView.as_view(), name='todo-api-view'),
    path('todo-nested/', TodoAPIView.as_view(), name='todo-api-view'),
    path('bulk-todo-nested/', BulkTodoAPIView.as_view(), name='bulk-todo-api-view'),
]
