from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Min, Max, Count, Q
from django.contrib.auth import get_user_model

from .models import Task, ReviewAssignment, Review
from .serializers import (
    TaskCreateSerializer, TaskListSerializer,
    ReviewAssignmentListSerializer, ReviewCreateSerializer
)
from .services import generate_random_assignments

User = get_user_model()

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            # فقط ادمین می‌تواند وزن‌ها را هنگام ساخت یا ویرایش تغییر دهد
            if self.request.user.is_staff:
                return TaskCreateSerializer
        return TaskListSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Task.objects.all().order_by('-created_at')
        return Task.objects.filter(owner=self.request.user).order_by('-created_at')

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def lock_all(self, request):
        Task.objects.filter(locked=False).update(locked=True)
        return Response({"status": "تمام تکالیف با موفقیت قفل شدند."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def assign_all(self, request):
        try:
            k = int(request.data.get("k", 10))
            generate_random_assignments(k=k)
            return Response({"status": f"تخصیص ارزیابی برای {k} داور برای هر تکلیف آغاز شد."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"], url_path='summary')
    def summary(self, request, pk=None):
        task = self.get_object()
        reviews = Review.objects.filter(assignment__task=task)
        if not reviews.exists():
            return Response({"count": 0})
        
        summary_data = reviews.aggregate(
            mean_score=Avg("weighted_total"),
            min_score=Min("weighted_total"),
            max_score=Max("weighted_total")
        )
        return Response({
            "count": reviews.count(),
            "mean": round(summary_data["mean_score"], 2),
            "min": summary_data["min_score"],
            "max": summary_data["max_score"],
        })


class ReviewAssignmentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewAssignmentListSerializer

    def get_queryset(self):
        return ReviewAssignment.objects.filter(reviewer=self.request.user).select_related('task', 'task__owner').order_by('id')


class ReviewViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewCreateSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Review.objects.all().select_related('assignment__task', 'assignment__reviewer')
            
        # کاربر می‌تواند نقدهایی که خودش ثبت کرده یا نقدهای مربوط به تکلیف خودش را ببیند
        return Review.objects.filter(
            Q(assignment__reviewer=self.request.user) |
            Q(assignment__task__owner=self.request.user)
        ).select_related('assignment__task', 'assignment__reviewer')


