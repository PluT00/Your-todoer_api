from django.contrib import admin
from your_todoer_api.models import Task, Project


class ProjectAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'owner'
    ]


class TaskAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'is_completed',
        'user'
    ]

admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
