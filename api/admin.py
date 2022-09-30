from django.contrib import admin

from .models import Task, Todo, Tag, PostTag, Post


admin.site.register(Todo)
admin.site.register(Task)
admin.site.register(Tag)
# admin.site.register(Post)
admin.site.register(PostTag)

class TagAdminInline(admin.TabularInline):
    model = PostTag
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'published')
    inlines = (TagAdminInline,)
