from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm


def dashboard(request):
    context = {
        "task_count": Task.objects.count(),
        "pending_count": Task.objects.filter(status="Pending").count(),
        "in_progress_count": Task.objects.filter(status="In Progress").count(),
        "completed_count": Task.objects.filter(status="Completed").count(),
    }
    return render(request, "tasks/dashboard.html", context)


def task_list(request):
    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks": tasks})


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "tasks/task_detail.html", {"task": task})


def task_create(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("task_list")

    return render(request, "tasks/task_form.html", {"form": form})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)

    if form.is_valid():
        form.save()
        return redirect("task_detail", pk=pk)

    return render(request, "tasks/task_form.html", {"form": form})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    return render(request, "tasks/task_confirm_delete.html", {"task": task})