from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    """تکلیف آپلودی هر دانش‌آموز"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    file = models.FileField(upload_to="tasks/")
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    locked = models.BooleanField(default=False)

    # فیلدهای جدید برای وزن‌های داینامیک
    nezm_weight = models.FloatField(default=0.2, help_text="وزن معیار نظم (مثال: 0.2 برای 20%)")
    khalaghiat_weight = models.FloatField(default=0.3, help_text="وزن معیار خلاقیت (مثال: 0.3 برای 30%)")
    elmi_weight = models.FloatField(default=0.5, help_text="وزن معیار علمی بودن (مثال: 0.5 برای 50%)")

    def clean(self):
        # اعتبارسنجی برای اطمینان از اینکه مجموع وزن‌ها برابر ۱ است
        total_weight = self.nezm_weight + self.khalaghiat_weight + self.elmi_weight
        if abs(total_weight - 1.0) > 0.001:
            raise ValidationError("مجموع وزن‌های معیارها باید دقیقاً برابر با ۱ باشد.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.owner.username})"

class ReviewAssignment(models.Model):
    """تخصیص «چه کسی باید تکلیف چه کسی را ارزیابی کند»."""
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_assignments")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="assignments")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reviewer", "task")

    def __str__(self):
        return f"{self.reviewer.username} -> {self.task_id}"

class Review(models.Model):
    """امتیازاتی که reviewer به task داده است."""
    assignment = models.OneToOneField(ReviewAssignment, on_delete=models.CASCADE, related_name="review")
    nezm = models.PositiveIntegerField()
    khalaghiat = models.PositiveIntegerField()
    elmi = models.PositiveIntegerField()
    weighted_total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def compute_weighted(self) -> float:
        # خواندن وزن‌ها به صورت داینامیک از تکلیف مرتبط
        task = self.assignment.task
        return (
            self.nezm * task.nezm_weight +
            self.khalaghiat * task.khalaghiat_weight +
            self.elmi * task.elmi_weight
        )

    def save(self, *args, **kwargs):
        self.weighted_total = self.compute_weighted()
        super().save(*args, **kwargs)

