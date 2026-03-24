from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm, SubTaskForm, NoteForm


def dashboard(request):
    recent_tasks = Task.objects.select_related("priority", "category").order_by("-created_at")[:5]
    upcoming_tasks = Task.objects.select_related("priority", "category").order_by("deadline")[:5]

    context = {
        "task_count": Task.objects.count(),
        "pending_count": Task.objects.filter(status="Pending").count(),
        "in_progress_count": Task.objects.filter(status="In Progress").count(),
        "completed_count": Task.objects.filter(status="Completed").count(),
        "recent_tasks": recent_tasks,
        "upcoming_tasks": upcoming_tasks,
    }
    return render(request, "tasks/dashboard.html", context)


def task_list(request):
    query = request.GET.get("q", "")
    status = request.GET.get("status", "")

    tasks = Task.objects.select_related("priority", "category").all()

    if query:
        tasks = tasks.filter(title__icontains=query)

    if status:
        tasks = tasks.filter(status=status)

    tasks = tasks.order_by("deadline")

    return render(request, "tasks/task_list.html", {
        "tasks": tasks,
        "query": query,
        "status": status,
    })


def task_detail(request, pk):
    task = get_object_or_404(Task.objects.select_related("priority", "category"), pk=pk)
    subtask_form = SubTaskForm(initial={"task": task})
    note_form = NoteForm(initial={"task": task})

    return render(request, "tasks/task_detail.html", {
        "task": task,
        "subtask_form": subtask_form,
        "note_form": note_form,
    })


def task_create(request):
    form = TaskForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("task_list")

    return render(request, "tasks/task_form.html", {
        "form": form,
        "page_title": "Create Task",
    })


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)

    if form.is_valid():
        form.save()
        return redirect("task_detail", pk=task.pk)

    return render(request, "tasks/task_form.html", {
        "form": form,
        "page_title": "Edit Task",
    })


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    return render(request, "tasks/task_confirm_delete.html", {"task": task})


def subtask_create(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = SubTaskForm(request.POST or None)

    if form.is_valid():
        subtask = form.save(commit=False)
        subtask.task = task
        subtask.save()
        return redirect("task_detail", pk=task.pk)

    return render(request, "tasks/task_detail.html", {
        "task": task,
        "subtask_form": form,
        "note_form": NoteForm(initial={"task": task}),
    })


def note_create(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = NoteForm(request.POST or None)

    if form.is_valid():
        note = form.save(commit=False)
        note.task = task
        note.save()
        return redirect("task_detail", pk=task.pk)

    return render(request, "tasks/task_detail.html", {
        "task": task,
        "subtask_form": SubTaskForm(initial={"task": task}),
        "note_form": form,
    })