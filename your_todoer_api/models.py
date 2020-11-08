from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=500)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name="projects")

    def __str__(self):
        return f'{self.owner.username} | {self.name}'


class Task(models.Model):
    title = models.CharField(max_length=1500)
    is_completed = models.BooleanField(default=False)
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name="tasks")
    owner = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="tasks")

    def __str__(self):
        return f'{self.owner.username} | {self.project.name}:{self.title}'
