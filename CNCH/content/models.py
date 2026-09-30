from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class MentorSection(models.Model):
    
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} — {self.mentor.username}"

class Video(models.Model):
    section = models.ForeignKey(MentorSection, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/')  
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserFile(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    file = models.FileField(upload_to='user_files/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uploader.username} - {self.file.name}"
class LearningContent(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('video', 'ویدیو آموزشی'),
        ('document', 'سند / جزوه دانلودی'),
        ('link', 'لینک خارجی'),
    ]
    title = models.CharField(max_length=255, verbose_name="عنوان محتوا")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='video', verbose_name="نوع محتوا")
    file = models.FileField(upload_to='learning_contents/', null=True, blank=True, verbose_name="فایل ضمیمه یا ویدیو")
    video_url = models.URLField(blank=True, null=True, verbose_name="لینک آنلاین ویدیو (آپارات، یوتیوب، و...)")
    is_public = models.BooleanField(default=True, verbose_name="عمومی (قابل مشاهده برای همه)")
    allowed_groups = models.ManyToManyField('account.SchoolGroup', blank=True, related_name='allowed_contents', verbose_name="گروه‌های اختصاصی مجاز")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ بارگذاری")

    class Meta:
        verbose_name = "محتوای آموزشی"
        verbose_name_plural = "محتواهای آموزشی"
        ordering = ['-created_at']

    def __str__(self):
        return self.title