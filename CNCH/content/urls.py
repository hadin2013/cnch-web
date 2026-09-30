from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload-file/', views.upload_user_file, name='upload_user_file'),
    path('mentor/create-section/', views.create_section, name='create_section'),
    path('mentor/upload-video/', views.upload_video, name='upload_video'),
    path('video/<int:pk>/', views.watch_video, name='watch_video'),
    path('mentor/users/', views.list_normal_users, name='list_normal_users'),
    path('api/contents/', views.LearningContentListView.as_view(), name='learning-contents-api'),
]
