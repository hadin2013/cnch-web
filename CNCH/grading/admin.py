from django.contrib import admin
from .models import Task, ReviewAssignment, Review

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at', 'locked', 'nezm_weight', 'khalaghiat_weight', 'elmi_weight')
    list_filter = ('locked', 'created_at')
    search_fields = ('title', 'owner__username')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'owner', 'file', 'locked')
        }),
        ('پیکربندی معیارها (مجموع باید ۱ شود)', {
            'fields': ('nezm_weight', 'khalaghiat_weight', 'elmi_weight'),
            'description': 'وزن هر معیار را به صورت اعشاری وارد کنید. مثال: 0.2 برای 20 درصد.'
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('get_task_title', 'get_reviewer', 'weighted_total', 'created_at')
    readonly_fields = ('weighted_total',)
    search_fields = ('assignment__task__title', 'assignment__reviewer__username')

    @admin.display(description='Task Title')
    def get_task_title(self, obj):
        return obj.assignment.task.title
    
    @admin.display(description='Reviewer')
    def get_reviewer(self, obj):
        return obj.assignment.reviewer.username

@admin.register(ReviewAssignment)
class ReviewAssignmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'reviewer', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('task__title', 'reviewer__username')


