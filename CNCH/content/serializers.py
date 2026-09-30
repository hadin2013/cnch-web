from rest_framework import serializers
from .models import LearningContent

class LearningContentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = LearningContent
        fields = ['id', 'title', 'description', 'content_type', 'file_url', 'video_url', 'is_public', 'created_at']

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.file.url) if request else obj.file.url
        return None