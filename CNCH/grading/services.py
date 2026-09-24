import random
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Task, ReviewAssignment

User = get_user_model()

def _task_id_by_owner(tasks, owner_id):
    """Helper function to find task_id from a list of tasks by owner_id."""
    for t in tasks:
        if t.owner_id == owner_id:
            return t.id
    raise ValueError(f"No task found for owner {owner_id}")


def generate_random_assignments(k: int = 10):
    """
    برای تمام تکالیفِ lock شده، به‌صورت رندوم assignment می‌سازد.
    """
    tasks = list(Task.objects.filter(locked=True))
    users_with_tasks = list(User.objects.filter(tasks__in=tasks).distinct())

    if not tasks or not users_with_tasks:
        print("No locked tasks or users with tasks to assign.")
        return

    user_ids = [u.id for u in users_with_tasks]
    task_ids = [t.id for t in tasks]
    
    # نقشه هر کاربر به تکلیف خودش
    user_task_map = {task.owner_id: task.id for task in tasks}

    # اطمینان از اینکه همه کاربران تکلیف‌دار در نقشه هستند
    for user_id in user_ids:
        if user_id not in user_task_map:
            raise ValueError(f"User with ID {user_id} has no task in the locked set.")

    if len(user_ids) < 2:
        print("Warning: Not enough users to create non-self assignments.")
        return

    with transaction.atomic():
        ReviewAssignment.objects.filter(task__in=tasks).delete()
        assignments_to_create = []

        for task_to_be_reviewed in tasks:
            owner_id = task_to_be_reviewed.owner_id
            
            # لیست داوران بالقوه (همه به جز صاحب تکلیف)
            potential_reviewers = [uid for uid in user_ids if uid != owner_id]
            
            # اگر تعداد داوران بالقوه کمتر از k است، از همه آنها استفاده کن
            num_reviewers_to_select = min(k, len(potential_reviewers))

            if num_reviewers_to_select < k:
                print(f"Warning: Task {task_to_be_reviewed.id} will be assigned only {num_reviewers_to_select} times, less than the desired {k}.")

            # انتخاب k داور به صورت رندوم
            selected_reviewer_ids = random.sample(potential_reviewers, num_reviewers_to_select)

            for reviewer_id in selected_reviewer_ids:
                assignments_to_create.append(
                    ReviewAssignment(reviewer_id=reviewer_id, task=task_to_be_reviewed)
                )

        ReviewAssignment.objects.bulk_create(assignments_to_create)
        print(f"Successfully created {len(assignments_to_create)} new review assignments.")


