from django.contrib import admin
from your_todoer_api.models import Task


class TaskAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'is_completed',
        'user'
    ]

admin.site.register(Task, TaskAdmin)
