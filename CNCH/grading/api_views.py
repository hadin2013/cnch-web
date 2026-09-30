from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Assignment, AssignmentSubmission

class AssignmentSerializer(serializers.ModelSerializer):
    attachment_url = serializers.SerializerMethodField()
    my_submission = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'attachment_url', 'due_date', 'max_score', 'is_active', 'my_submission']

    def get_attachment_url(self, obj):
        if obj.attachment:
            req = self.context.get('request')
            return req.build_absolute_uri(obj.attachment.url) if req else obj.attachment.url
        return None

    def get_my_submission(self, obj):
        req = self.context.get('request')
        if not req or not req.user.is_authenticated:
            return None
        submission = obj.submissions.filter(user=req.user).first()
        if not submission:
            return None
        return {
            'id': submission.id,
            'submission_file_url': req.build_absolute_uri(submission.submission_file.url) if submission.submission_file else None,
            'comment': submission.comment,
            'status': submission.status,
            'score': submission.score,
            'feedback': submission.feedback,
            'submitted_at': submission.submitted_at
        }

class AssignmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        group_ids = []
        if hasattr(user, 'student_profile') and user.student_profile.school_group_id:
            group_ids.append(user.student_profile.school_group_id)
        if hasattr(user, 'organized_groups'):
            group_ids.extend(user.organized_groups.values_list('id', flat=True))

        q = Q(allowed_groups__isnull=True)
        if group_ids:
            q |= Q(allowed_groups__id__in=group_ids)

        assignments = Assignment.objects.filter(is_active=True).filter(q).distinct()
        serializer = AssignmentSerializer(assignments, many=True, context={'request': request})
        return Response(serializer.data)

class AssignmentSubmissionUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, assignment_id):
        try:
            assignment = Assignment.objects.get(id=assignment_id, is_active=True)
        except Assignment.DoesNotExist:
            return Response({'error': 'تکلیف موردنظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({'error': 'هیچ فایلی ارسال نشده است.'}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی حجم (حداکثر 50 مگابایت)
        if uploaded_file.size > 50 * 1024 * 1024:
            return Response({'error': 'حجم فایل نباید بیش از ۵۰ مگابایت باشد.'}, status=status.HTTP_400_BAD_REQUEST)

        group = None
        if hasattr(request.user, 'student_profile'):
            group = request.user.student_profile.school_group
        elif request.user.organized_groups.exists():
            group = request.user.organized_groups.first()

        submission, _ = AssignmentSubmission.objects.get_or_create(
            assignment=assignment,
            user=request.user,
            defaults={'group': group}
        )
        submission.submission_file = uploaded_file
        submission.comment = request.data.get('comment', '')
        submission.group = group
        submission.status = 'submitted'
        submission.save()

        return Response({'message': 'تکلیف با موفقیت ارسال شد.'}, status=status.HTTP_200_OK)