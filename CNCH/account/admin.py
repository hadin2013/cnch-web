from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SchoolGroup, Student, Ticket

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'national_id', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'national_id', 'phone_number', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات اختصاصی', {'fields': ('role', 'national_id', 'phone_number', 'user_credit', 'address')}),
    )

admin.site.register(User, CustomUserAdmin)

class StudentInline(admin.TabularInline):
    model = Student
    extra = 0
    readonly_fields = ('get_national_id', 'get_phone', 'get_email')
    
    def get_national_id(self, obj):
        return obj.user.national_id if obj.user else '-'
    get_national_id.short_description = 'کد ملی'

    def get_phone(self, obj):
        return obj.user.phone_number if obj.user else '-'
    get_phone.short_description = 'شماره تماس'

    def get_email(self, obj):
        return obj.user.email if obj.user else '-'
    get_email.short_description = 'ایمیل'

@admin.register(SchoolGroup)
class SchoolGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'school_name', 'city', 'province', 'get_organizer_name', 'get_organizer_phone', 'get_organizer_email', 'finalized')
    list_filter = ('province', 'finalized')
    search_fields = ('group_name', 'school_name', 'city', 'organizer__first_name', 'organizer__last_name', 'organizer__phone_number', 'organizer__email')
    inlines = [StudentInline]

    def get_organizer_name(self, obj):
        if obj.organizer:
            return f"{obj.organizer.first_name} {obj.organizer.last_name}" or obj.organizer.username
        return '-'
    get_organizer_name.short_description = 'سرگروه'

    def get_organizer_phone(self, obj):
        return obj.organizer.phone_number if obj.organizer else '-'
    get_organizer_phone.short_description = 'شماره تماس سرگروه'

    def get_organizer_email(self, obj):
        return obj.organizer.email if obj.organizer else '-'
    get_organizer_email.short_description = 'ایمیل سرگروه'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_national_id', 'get_phone', 'get_email', 'school_group', 'grade', 'major')
    list_filter = ('grade', 'major', 'school_group__province')
    search_fields = ('user__first_name', 'user__last_name', 'user__national_id', 'user__phone_number', 'user__email', 'school_group__group_name')

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}" if obj.user else '-'
    get_full_name.short_description = 'نام و نام خانوادگی'

    def get_national_id(self, obj):
        return obj.user.national_id if obj.user else '-'
    get_national_id.short_description = 'کد ملی'

    def get_phone(self, obj):
        return obj.user.phone_number if obj.user else '-'
    get_phone.short_description = 'شماره تماس'

    def get_email(self, obj):
        return obj.user.email if obj.user else '-'
    get_email.short_description = 'ایمیل'

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'get_user_phone', 'created_at', 'resolved')
    list_filter = ('resolved', 'created_at')
    search_fields = ('title', 'message', 'user__username', 'user__email', 'user__phone_number')
    list_editable = ('resolved',)

    def get_user_phone(self, obj):
        return obj.user.phone_number if obj.user else '-'
    get_user_phone.short_description = 'تلفن تماس'
