from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "note", "due_at", "is_done"]
        widgets = {"due_at": forms.DateTimeInput(attrs={"type": "datetime-local"})}
