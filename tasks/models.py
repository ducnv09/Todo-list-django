from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    note = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    due_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["is_done", "-created_at"]

    def __str__(self):
        return self.title
