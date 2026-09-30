from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ReviewAssignmentViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"review-assignments", ReviewAssignmentViewSet, basename="review-assignment")
router.register(r"reviews", ReviewViewSet, basename="review")

urlpatterns = [
    path("", include(router.urls)),
]

from .api_views import AssignmentListView, AssignmentSubmissionUploadView

urlpatterns += [
    path('assignments/', AssignmentListView.as_view(), name='assignment-list'),
    path('assignments/<int:assignment_id>/submit/', AssignmentSubmissionUploadView.as_view(), name='assignment-submit'),
]