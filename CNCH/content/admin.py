from django.contrib import admin

# Register your models here.
from .models import LearningContent

@admin.register(LearningContent)
class LearningContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'is_public', 'created_at')
    list_filter = ('content_type', 'is_public')
    search_fields = ('title', 'description')
    filter_horizontal = ('allowed_groups',)