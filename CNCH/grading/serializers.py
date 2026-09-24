from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task, ReviewAssignment, Review

User = get_user_model()

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "file", "nezm_weight", "khalaghiat_weight", "elmi_weight"]

    def create(self, validated_data):
        return Task.objects.create(owner=self.context["request"].user, **validated_data)

    def validate(self, data):
        total_weight = (
            data.get("nezm_weight", 0.2) +
            data.get("khalaghiat_weight", 0.3) +
            data.get("elmi_weight", 0.5)
        )
        if abs(total_weight - 1.0) > 0.001:
            raise serializers.ValidationError("مجموع وزن‌های معیارها باید دقیقاً برابر با ۱ باشد.")
        return data

class TaskListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    received_reviews = serializers.SerializerMethodField()
    mean_score = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id", "title", "file", "created_at", "locked", "owner",
            "nezm_weight", "khalaghiat_weight", "elmi_weight",
            "received_reviews", "mean_score"
        ]

    def get_received_reviews(self, obj):
        return obj.assignments.filter(review__isnull=False).count()

    def get_mean_score(self, obj):
        reviews = Review.objects.filter(assignment__task=obj)
        if not reviews.exists():
            return None
        return round(sum(r.weighted_total for r in reviews) / reviews.count(), 2)

class ReviewAssignmentListSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source="task.title", read_only=True)
    task_owner = serializers.CharField(source="task.owner.username", read_only=True)
    task_file_url = serializers.FileField(source="task.file", read_only=True)
    has_review = serializers.SerializerMethodField()

    class Meta:
        model = ReviewAssignment
        fields = ["id", "task", "task_title", "task_owner", "task_file_url", "created_at", "has_review"]

    def get_has_review(self, obj):
        return hasattr(obj, "review")

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "assignment", "nezm", "khalaghiat", "elmi", "weighted_total"]
        read_only_fields = ["weighted_total"]

    def validate(self, attrs):
        for f in ["nezm", "khalaghiat", "elmi"]:
            if attrs.get(f) < 0 or attrs.get(f) > 100:
                raise serializers.ValidationError(f"{f} must be between 0 and 100.")
        return attrs

    def create(self, validated_data):
        assignment = validated_data["assignment"]
        request = self.context["request"]
        if assignment.reviewer_id != request.user.id:
            raise serializers.ValidationError("You are not the reviewer for this assignment.")
        if hasattr(assignment, "review"):
            raise serializers.ValidationError("You already reviewed this assignment.")
        return super().create(validated_data)

