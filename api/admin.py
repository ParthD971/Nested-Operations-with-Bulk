from django.contrib import admin

from .models import Task, Todo


admin.site.register(Todo)
admin.site.register(Task)