from django.urls import path
from .views import TaskAPIView, TodoAPIView, BulkTodoAPIView, PostAPIView, BookDetailsAPIView

urlpatterns = [
    path('todo-nested/', TodoAPIView.as_view(), name='todo-api-view'),
    path('task-nested/', TaskAPIView.as_view(), name='task-api-view'),
    path('bulk-todo-nested/', BulkTodoAPIView.as_view(), name='bulk-todo-api-view'),

    path('post/', PostAPIView.as_view(), name='post-api-view'),

    path('book-details/', BookDetailsAPIView.as_view(), name='book-details-api-view'),


]
