from django.shortcuts import render, get_object_or_404
from .models import Task


def dashboard(request):
    context = {
        "task_count": Task.objects.count(),
        "pending_count": Task.objects.filter(status="Pending").count(),
        "in_progress_count": Task.objects.filter(status="In Progress").count(),
        "completed_count": Task.objects.filter(status="Completed").count(),
        "recent_tasks": Task.objects.select_related("priority", "category").order_by("-created_at")[:5],
    }
    return render(request, "tasks/dashboard.html", context)


def task_list(request):
    tasks = Task.objects.select_related("priority", "category").all()
    return render(request, "tasks/task_list.html", {"tasks": tasks})


def task_detail(request, pk):
    task = get_object_or_404(
        Task.objects.select_related("priority", "category"),
        pk=pk,
    )
    return render(request, "tasks/task_detail.html", {"task": task})