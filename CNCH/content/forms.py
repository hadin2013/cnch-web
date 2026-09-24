from django import forms
from .models import UserFile, Video, MentorSection

class UserFileForm(forms.ModelForm):
    class Meta:
        model = UserFile
        fields = ['file', 'description']

class MentorSectionForm(forms.ModelForm):
    class Meta:
        model = MentorSection
        fields = ['title', 'description']

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['section', 'title', 'video_file']
