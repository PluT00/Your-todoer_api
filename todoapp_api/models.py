from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=1500)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="tasks")

    def __str__(self):
        return f'{self.id} | {self.title}'
