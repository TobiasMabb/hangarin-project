import os
import random
import django

from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hangarin.settings")
django.setup()

from django.utils import timezone
from tasks.models import Category, Priority, Task, SubTask, Note


fake = Faker()


def seed_reference_data():
    priorities = ["High", "Medium", "Low", "Critical", "Optional"]
    categories = ["Work", "School", "Personal", "Finance", "Projects"]

    for priority_name in priorities:
        Priority.objects.get_or_create(name=priority_name)

    for category_name in categories:
        Category.objects.get_or_create(name=category_name)

    print("Priority and Category records added.")


def seed_fake_data(task_count=15):
    priority_ids = list(Priority.objects.values_list("id", flat=True))
    category_ids = list(Category.objects.values_list("id", flat=True))
    statuses = ["Pending", "In Progress", "Completed"]

    if not priority_ids or not category_ids:
        print("Please seed Priority and Category first.")
        return

    for _ in range(task_count):
        deadline = timezone.make_aware(fake.date_time_this_month())

        task = Task.objects.create(
            title=fake.sentence(nb_words=5),
            description=fake.paragraph(nb_sentences=3),
            status=fake.random_element(elements=statuses),
            deadline=deadline,
            priority_id=random.choice(priority_ids),
            category_id=random.choice(category_ids),
        )

        subtask_count = random.randint(2, 5)
        for _ in range(subtask_count):
            SubTask.objects.create(
                task=task,
                title=fake.sentence(nb_words=4),
                status=fake.random_element(elements=statuses),
            )

        note_count = random.randint(1, 3)
        for _ in range(note_count):
            Note.objects.create(
                task=task,
                content=fake.paragraph(nb_sentences=2),
            )

    print(f"{task_count} tasks with subtasks and notes added.")


if __name__ == "__main__":
    seed_reference_data()
    seed_fake_data()
    print("Seeding completed successfully.")