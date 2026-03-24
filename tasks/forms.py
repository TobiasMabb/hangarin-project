from django import forms
from .models import Task, SubTask, Note


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = Task
        fields = ["title", "description", "status", "deadline", "priority", "category"]


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ["task", "title", "status"]


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["task", "content"]