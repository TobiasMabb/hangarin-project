from django import forms
from .models import Task, SubTask, Note


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = Task
        fields = ["title", "description", "status", "deadline", "priority", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "priority": forms.Select(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ["title", "status"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }