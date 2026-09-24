from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import MentorSection, Video, UserFile
from .forms import UserFileForm, MentorSectionForm, VideoUploadForm
from account.utils import role_required, roles_required

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'content/home.html')

@login_required
def dashboard(request):
    # هر نقش داشبورد متفاوت می‌بینه
    if request.user.role == 'mentor':
        sections = MentorSection.objects.filter(mentor=request.user)
        return render(request, 'content/mentor_dashboard.html', {'sections': sections})
    else:
        # normal user: لیست ویدیوها (یا ویدیوهای همهٔ منتورها)
        videos = Video.objects.select_related('section__mentor').all()
        return render(request, 'content/normal_dashboard.html', {'videos': videos})

@login_required
def upload_user_file(request):
    if request.method == 'POST':
        form = UserFileForm(request.POST, request.FILES)
        if form.is_valid():
            uf = form.save(commit=False)
            uf.uploader = request.user
            uf.save()
            return redirect('dashboard')
    else:
        form = UserFileForm()
    return render(request, 'content/upload_user_file.html', {'form': form})

@role_required('mentor')
def create_section(request):
    if request.method == 'POST':
        form = MentorSectionForm(request.POST)
        if form.is_valid():
            sec = form.save(commit=False)
            sec.mentor = request.user
            sec.save()
            return redirect('dashboard')
    else:
        form = MentorSectionForm()
    return render(request, 'content/create_section.html', {'form': form})

@role_required('mentor')
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        # ensure section belongs to mentor
        if form.is_valid():
            video = form.save(commit=False)
            if video.section.mentor != request.user:
                return render(request, '403.html', status=403)
            video.save()
            return redirect('dashboard')
    else:
        form = VideoUploadForm()
        # محدود کردن سشن‌ها به سشن‌های منتور فعلی:
        form.fields['section'].queryset = MentorSection.objects.filter(mentor=request.user)
    return render(request, 'content/upload_video.html', {'form': form})

# نمایش ویدیو (قابل دسترسی برای normal و mentor; admin هم)
@login_required
def watch_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    return render(request, 'content/watch_video.html', {'video': video})

# صفحهٔ لیست یوزرهای معمولی (منتور می‌تونه ببینه)
@roles_required('mentor')
def list_normal_users(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    normals = User.objects.filter(role='normal')
    return render(request, 'content/normal_users_list.html', {'users': normals})
