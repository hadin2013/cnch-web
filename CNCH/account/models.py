from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.core.validators import RegexValidator
from django.conf import settings


def generate_email_activation_code():
    return get_random_string(64)

class User(AbstractUser):
    ROLE_CHOICES = [('normal', 'Normal User'),('mentor', 'Mentor'),('admin', 'Admin'),]

    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی")
    national_id = models.CharField(max_length=10, unique=True, null=True, blank=True, verbose_name="کد ملی",
        validators=[RegexValidator(r'^\d{10}$', message="کد ملی باید ۱۰ رقم باشد")])
    phone_number = models.CharField(max_length=20, verbose_name="تلفن همراه", 
        validators=[RegexValidator(r'^\+?\d{10,20}$', message="شماره تلفن نامعتبر است")])
    email = models.EmailField(unique=True)
    email_active_code = models.CharField(max_length=64, default=generate_email_activation_code)
    is_email_activated = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)    
    user_credit = models.IntegerField(default=0)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='normal')

    def __str__(self):
        return self.get_full_name() or self.username

    def is_mentor(self):
        return self.role == 'mentor'

    def is_normal(self):
        return self.role == 'normal'

class SchoolGroup(models.Model):
    group_name = models.CharField(max_length=255, verbose_name="نام گروه")
    province = models.CharField(max_length=100, verbose_name="استان")
    city = models.CharField(max_length=100, verbose_name="شهر/شهرستان")
    school_name = models.CharField(max_length=255, verbose_name="نام مدرسه")
    school_phone = models.CharField(max_length=20, verbose_name="تلفن مدرسه",
        validators=[RegexValidator(r'^\+?\d{10,20}$', message="شماره تلفن نامعتبر است")])
    # the authenticated user who registered/owns this group (null for legacy groups)
    organizer = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='organized_groups', verbose_name="مسئول گروه")
    # whether the group creation has been finalized by the user (useful for payment hooks)
    finalized = models.BooleanField(default=False)
    # placeholder for external payment reference (درگاه پرداخت) to be filled later
    payment_reference = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.group_name} - {self.school_name}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="student_profile")
    school_group = models.ForeignKey(SchoolGroup, on_delete=models.CASCADE, related_name='students', verbose_name="گروه/مدرسه")
    grade = models.CharField(max_length=50, verbose_name="پایه تحصیلی")
    major = models.CharField(max_length=100, verbose_name="رشته تحصیلی")

    def __str__(self):
        return str(self.user)

class Ticket(models.Model):
    """Simple ticket model for users to contact admins about conflicts or issues."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Ticket #{self.pk} by {self.user.get_full_name() or self.user.username} - {self.title}"
