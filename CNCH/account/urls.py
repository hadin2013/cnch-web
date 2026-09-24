from django.urls import path
from . import views

urlpatterns = [
    # auth & profile
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/change-password/', views.PasswordChangeView.as_view(), name='change-password'),
    path('profile/tickets/', views.ProfileTicketCreateView.as_view(), name='profile-ticket-create'),

    # students & groups (competition registration)
    path('students/', views.StudentCreateView.as_view(), name='student-create'),
    path('students/<int:pk>/', views.StudentUpdateView.as_view(), name='student-update'),
    path('groups/', views.SchoolGroupCreateView.as_view(), name='group-create'),
    path('groups/<int:pk>/', views.SchoolGroupDashboardView.as_view(), name='group-dashboard'),

    # admin panel
    path('admin/users/', views.AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/<int:pk>/', views.AdminUserUpdateView.as_view(), name='admin-user-update'),
    path('admin/groups/', views.AdminGroupListView.as_view(), name='admin-group-list'),
    path('admin/tickets/', views.AdminTicketListView.as_view(), name='admin-ticket-list'),
    path('admin/tickets/<int:pk>/resolve/', views.AdminTicketResolveView.as_view(), name='admin-ticket-resolve'),
]
