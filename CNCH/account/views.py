from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Student, SchoolGroup, Ticket
from .permissions import IsAdminRole
from .serializers import (
    StudentSerializer, SchoolGroupDashboardSerializer, SchoolGroupCreateSerializer,
    UserSerializer, UserCreateSerializer, PasswordChangeSerializer,
    AdminUserRowSerializer, AdminUserUpdateSerializer, AdminGroupRowSerializer,
    TicketSerializer,
)

User = get_user_model()


# ---------------------------------------------------------------------------
# Signup / Profile
# ---------------------------------------------------------------------------

class SignupView(generics.CreateAPIView):
    """ثبت‌نام حساب کاربری (ایمیل + رمز عبور)."""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class ProfileView(APIView):
    """پروفایل کاربر خود + گروه/دانش‌آموزی که عضو آن است + تیکت‌هایش."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        payload = {
            "user": UserSerializer(user).data,
            "group": None,
            "student": None,
            "tickets": [],
        }
        # the most recent group this user organizes
        group = SchoolGroup.objects.filter(organizer=user).order_by('-id').first()
        if group:
            payload["group"] = SchoolGroupDashboardSerializer(group).data
        # this user's own student record (if any)
        student = getattr(user, 'student_profile', None)
        if student:
            payload["student"] = StudentSerializer(student).data
        payload["tickets"] = TicketSerializer(user.tickets.order_by('-created_at'), many=True).data
        return Response(payload)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(request.user).data)


class PasswordChangeView(APIView):
    """تغییر رمز عبور."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save(update_fields=['password'])
        return Response({"detail": "رمز عبور با موفقیت تغییر کرد."})


class ProfileTicketCreateView(generics.CreateAPIView):
    """ارسال تیکت جدید توسط کاربر واردشده."""
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ---------------------------------------------------------------------------
# Admin panel APIs (role == 'admin' or superuser)
# ---------------------------------------------------------------------------

class AdminUserListView(generics.ListAPIView):
    """لیست کاربران با جستجو (q) و فیلتر نقش (role)."""
    serializer_class = AdminUserRowSerializer
    permission_classes = [IsAdminRole]

    def get_queryset(self):
        qs = User.objects.all().order_by('-created_at')
        q = self.request.query_params.get('q')
        if q:
            qs = qs.filter(
                Q(username__icontains=q) | Q(email__icontains=q) |
                Q(first_name__icontains=q) | Q(last_name__icontains=q) |
                Q(national_id__icontains=q) | Q(phone_number__icontains=q))
        role = self.request.query_params.get('role')
        if role in dict(User.ROLE_CHOICES):
            qs = qs.filter(role=role)
        return qs


class AdminUserUpdateView(generics.UpdateAPIView):
    """ویرایش پروفایل/نقش یک کاربر توسط مدیر."""
    queryset = User.objects.all()
    serializer_class = AdminUserUpdateSerializer
    permission_classes = [IsAdminRole]
    http_method_names = ['patch', 'get', 'head']

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(AdminUserRowSerializer(instance).data)


class AdminGroupListView(generics.ListAPIView):
    """لیست گروه‌های مدارس با شمارش دانش‌آموزان."""
    serializer_class = AdminGroupRowSerializer
    permission_classes = [IsAdminRole]

    def get_queryset(self):
        qs = SchoolGroup.objects.order_by('-id')
        q = self.request.query_params.get('q')
        if q:
            qs = qs.filter(
                Q(group_name__icontains=q) |
                Q(school_name__icontains=q) |
                Q(city__icontains=q))
        return qs


class AdminTicketListView(generics.ListAPIView):
    """لیست تیکت‌های کاربران."""
    serializer_class = TicketSerializer
    permission_classes = [IsAdminRole]

    def get_queryset(self):
        qs = Ticket.objects.select_related('user').order_by('-created_at')
        if self.request.query_params.get('unresolved') == '1':
            qs = qs.filter(resolved=False)
        return qs


class AdminTicketResolveView(APIView):
    """باز/بسته کردن تیکت."""
    permission_classes = [IsAdminRole]

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        resolved = request.data.get('resolved')
        if not isinstance(resolved, bool):
            return Response({"resolved": "مقدار وضعیت باید true یا false باشد."}, status=status.HTTP_400_BAD_REQUEST)
        ticket.resolved = resolved
        ticket.save(update_fields=['resolved'])
        return Response(TicketSerializer(ticket).data)

class SchoolGroupCreateView(APIView):
    """     API ساخت گروه (مرحله اول)   """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SchoolGroupCreateSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            # link the authenticated user as group organizer (if signing in)
            if request.user.is_authenticated and not group.organizer:
                group.organizer = request.user
                group.save(update_fields=['organizer'])
                serializer = SchoolGroupCreateSerializer(group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentCreateView(generics.CreateAPIView):
    """     API ساخت دانش‌آموز (مرحله دوم)   """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = serializer.validated_data['school_group']
        if group.organizer_id != request.user.id and not (request.user.is_superuser or request.user.role == 'admin'):
            return Response({"school_group": "شما مسئول این گروه نیستید."}, status=status.HTTP_403_FORBIDDEN)
        student = serializer.save()
        return Response(serializer.to_representation(student), status=status.HTTP_201_CREATED)

class StudentUpdateView(generics.UpdateAPIView):
    """     API ویرایش دانش‌آموز     """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "pk"  # یا می‌توانی بنویسی "user_id" اگر متفاوت است

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        return Response(serializer.to_representation(student), status=status.HTTP_200_OK)

class SchoolGroupDashboardView(APIView):
    """     داشبورد گروه + لیست دانش‌آموزان  """
    def get(self, request, pk):
        group = get_object_or_404(SchoolGroup, pk=pk)
        serializer = SchoolGroupDashboardSerializer(group)
        return Response(serializer.data)





# from django.shortcuts import render, redirect , get_object_or_404
# from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.decorators import login_required
# from account.forms import ForgotPasswordForm, LoginForm, SignUpForm
# from account.models import User
# from django.contrib import messages
# from django.contrib.auth.decorators import user_passes_test
# from django.contrib.auth import get_user_model
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Student, SchoolGroup
# from .serializers import StudentCreateUpdateSerializer, SchoolGroupDashboardSerializer, SchoolGroupCreateSerializer
# from .forms import SchoolGroupForm, StudentFormSet
# from django.db import transaction
# from django.db.utils import IntegrityError

# @login_required
# def create_group(request):
#     """View for creating a school group and 3-6 students. Checks conflicts and allows sending a ticket to admin."""
#     if request.method == 'POST':
#         group_form = SchoolGroupForm(request.POST)
#         student_formset = StudentFormSet(request.POST)
#         if group_form.is_valid() and student_formset.is_valid():
#             group_name = group_form.cleaned_data['group_name']
#             # check duplicate group name (case-insensitive)
#             if SchoolGroup.objects.filter(group_name__iexact=group_name).exists():
#                 group_form.add_error('group_name', 'نام گروه تکراری است. لطفاً نام دیگری انتخاب کنید.')
#             else:
#                 # collect national ids
#                 national_ids = []
#                 cleaned_students = []
#                 for sform in student_formset:
#                     cd = sform.cleaned_data
#                     if not cd:
#                         continue
#                     nid = cd.get('national_id')
#                     if nid:
#                         national_ids.append(nid)
#                         cleaned_students.append(cd)

#                 # check for duplicates within submitted students
#                 if len(national_ids) != len(set(national_ids)):
#                     student_formset.non_form_errors = ['کد ملی تکراری در بین دانش‌آموزان وارد شده وجود دارد.']
#                 else:
#                     # find conflicts with existing students
#                     existing = Student.objects.filter(national_id__in=national_ids).values_list('national_id', flat=True)
#                     existing = list(existing)
#                     if existing:
#                         # conflict: show warning page (do not specify which student)
#                         request.session['pending_group'] = group_form.cleaned_data
#                         request.session['pending_students'] = cleaned_students
#                         request.session['conflict_count'] = len(existing)
#                         return render(request, 'account/group_conflict.html', {'conflict_count': len(existing)})

#                     # no conflicts: safe to create
#                     try:
#                         with transaction.atomic():
#                             group = group_form.save(commit=False)
#                             group.finalized = True  # finalized, payment to be added later
#                             group.save()
#                             for cd in cleaned_students:
#                                 Student.objects.create(school_group=group,
#                                                        first_name=cd.get('first_name'),
#                                                        last_name=cd.get('last_name'),
#                                                        national_id=cd.get('national_id'),
#                                                        phone_number=cd.get('phone_number'),
#                                                        grade=cd.get('grade'),
#                                                        major=cd.get('major'))
#                             messages.success(request, 'گروه با موفقیت ساخته شد. برای پرداخت مبلغ می‌توانید بعداً اقدام کنید.')
#                             return redirect('user_account')
#                     except IntegrityError:
#                         messages.error(request, 'خطا در ذخیره‌سازی اطلاعات. لطفاً دوباره تلاش کنید.')
#         # fall through to re-render
#     else:
#         group_form = SchoolGroupForm()
#         student_formset = StudentFormSet()
#     return render(request, 'account/create_group.html', {'group_form': group_form, 'student_formset': student_formset})


# @login_required
# def send_conflict_ticket(request):
#     """Create a ticket for admins when a conflict was detected during group creation."""
#     pending_group = request.session.get('pending_group')
#     pending_students = request.session.get('pending_students')
#     conflict_count = request.session.get('conflict_count', 0)
#     if request.method == 'POST':
#         # create a ticket summarizing the conflict; do not include identifying data
#         title = f"Conflict creating group: {pending_group.get('group_name') if pending_group else 'نامشخص'}"
#         message = f"کاربر درخواست ثبت گروه با {conflict_count} دانش‌آموزی که قبلاً در گروه دیگری ثبت شده‌اند را ارسال کرد."
#         from .models import Ticket
#         Ticket.objects.create(user=request.user, title=title, message=message)
#         # clear session
#         request.session.pop('pending_group', None)
#         request.session.pop('pending_students', None)
#         request.session.pop('conflict_count', None)
#         messages.success(request, 'تیکت به مدیریت ارسال شد. ما بزودی بررسی خواهیم کرد.')
#         return redirect('user_account')
#     return render(request, 'account/group_conflict.html', {'conflict_count': conflict_count})


# def user_login(request):
#     if request.method == 'POST':
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             username_or_email = login_form.cleaned_data["username_or_email"]
#             password = login_form.cleaned_data["password"]
#             remember_me = login_form.cleaned_data["remember_me"]

#             # Authenticate using username or email
#             user = authenticate(request, username=username_or_email, password=password)
#             if user is None:
#                 try:
#                     user = User.objects.get(email=username_or_email)
#                     user = authenticate(request, username=user.username, password=password)
#                 except User.DoesNotExist:
#                     user = None

#             if user is not None:
#                 login(request, user)
#                 if not remember_me:
#                     request.session.set_expiry(0)
#                 return redirect("user_account")
#             else:
#                 messages.error(request, 'Invalid username/email or password.')
#         else:
#             messages.error(request, 'Invalid form submission.')
#     else:
#         login_form = LoginForm()

#     return render(request, "account/login.html", {'login_form': login_form})

# def user_signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')  # Redirect to the login page after registration
#     else:
#         form = SignUpForm()
#     return render(request, 'account/signup.html', {'signup_form': form})

# def forgotpassword_page(request):
#     if request.method == "POST":
#         forgotpass_form = ForgotPasswordForm(request.POST)
#         if forgotpass_form.is_valid():
#             return redirect("index")
#         else:
#             pass

#     forgotpass_form = ForgotPasswordForm()
#     context = {'forgotpassword_from':forgotpass_form}
#     return render(request, "account/forgot-password.html", context=context)

# @login_required
# def user_account(request):
#     username = request.user
#     context = {"username":username}
#     return render(request, "account/user_account.html", context)

# def user_logout(request):
#     logout(request)
#     return redirect('login')


# def is_admin(user):
#     return user.is_authenticated and user.role == 'admin'

# @user_passes_test(is_admin)
# def promote_to_mentor(request, user_id):
#     User = get_user_model()
#     u = get_object_or_404(User, pk=user_id)
#     u.role = 'mentor'
#     u.save()
#     return redirect('user_account')


from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

class GroupRegistrationView(APIView):
    """
    ثبت‌نام یکپارچه دو مرحله‌ای:
    ۱. اعتبارسنجی ۱۰۰٪ داده‌ها قبل از نوشتن روی دیتابیس (بدون ساخت هیچ کاربری).
    ۲. ذخیره تراکنشی سرگروه، مدرسه و اعضا تنها در صورت موفقیت کامل مرحله اول.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        account_data = data.get('accountData')
        group_data = data.get('groupData')
        students_data = data.get('students') or []

        # ----------------------------------------------------
        # فاز ۱: اعتبارسنجی پیش‌دستانه (Zero-Write Validation)
        # ----------------------------------------------------
        if not group_data:
            return Response({'error': 'اطلاعات مدرسه و گروه الزامی است.'}, status=status.HTTP_400_BAD_REQUEST)
        if not students_data:
            return Response({'error': 'حداقل اطلاعات یک دانش‌آموز (سرگروه) باید وارد شود.'}, status=status.HTTP_400_BAD_REQUEST)
        if len(students_data) > 6:
            return Response({'error': 'حداکثر ظرفیت هر گروه ۶ دانش‌آموز است.'}, status=status.HTTP_400_BAD_REQUEST)

        # ۱. اعتبارسنجی سرگروه
        is_new_leader = not (request.user and request.user.is_authenticated)
        l_nid = ''
        l_email = ''
        l_password = ''
        l_first_name = ''
        l_last_name = ''
        l_phone = ''

        if is_new_leader:
            if not account_data:
                return Response({'error': 'اطلاعات حساب کاربری سرگروه الزامی است.'}, status=status.HTTP_400_BAD_REQUEST)
            l_nid = str(account_data.get('national_id', '')).strip()
            l_email = str(account_data.get('email', '')).strip().lower()
            l_password = str(account_data.get('password', ''))
            l_first_name = str(account_data.get('first_name', '')).strip()
            l_last_name = str(account_data.get('last_name', '')).strip()
            l_phone = str(account_data.get('phone_number', '')).strip()

            if not l_nid or len(l_nid) != 10 or not l_nid.isdigit():
                return Response({'error': 'کد ملی سرگروه باید ۱۰ رقم باشد.'}, status=status.HTTP_400_BAD_REQUEST)
            if not l_email or '@' not in l_email:
                return Response({'error': 'ایمیل سرگروه نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)
            if not l_password or len(l_password) < 6:
                return Response({'error': 'رمز عبور سرگروه باید حداقل ۶ کاراکتر باشد.'}, status=status.HTTP_400_BAD_REQUEST)
            if not l_phone or len(l_phone) < 10:
                return Response({'error': 'شماره موبایل سرگروه نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)

            # بررسی تکراری نبودن سرگروه در دیتابیس
            if User.objects.filter(Q(national_id=l_nid) | Q(username=l_nid)).exists():
                return Response({'error': f'کاربری با کد ملی {l_nid} قبلاً در سامانه ثبت شده است.'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email__iexact=l_email).exists():
                return Response({'error': f'کاربری با ایمیل {l_email} قبلاً ثبت شده است.'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(phone_number=l_phone).exists():
                return Response({'error': f'کاربری با شماره موبایل {l_phone} قبلاً ثبت شده است.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            leader_user = request.user
            l_nid = str(leader_user.national_id or leader_user.username).strip()
            l_phone = str(leader_user.phone_number or '').strip()

        # ۲. اعتبارسنجی تمامی اعضا (تکراری نبودن در فرم و دیتابیس)
        seen_nids = set()
        seen_phones = set()
        if l_nid:
            seen_nids.add(l_nid)
        if l_phone:
            seen_phones.add(l_phone)

        for idx, s in enumerate(students_data):
            s_nid = str(s.get('national_id', '')).strip()
            s_first = str(s.get('first_name', '')).strip()
            s_last = str(s.get('last_name', '')).strip()
            s_phone = str(s.get('phone_number', '')).strip()
            s_name = f"{s_first} {s_last}".strip() or f"عضو شماره {idx + 1}"

            if not s_nid or len(s_nid) != 10 or not s_nid.isdigit():
                return Response({'error': f'کد ملی {s_name} باید ۱۰ رقم باشد.'}, status=status.HTTP_400_BAD_REQUEST)
            if not s_phone or len(s_phone) < 10:
                return Response({'error': f'شماره موبایل {s_name} نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)

            is_leader = (idx == 0 or s_nid == l_nid)

            if not is_leader:
                # تکراری بودن در همین فرم
                if s_nid in seen_nids:
                    return Response({'error': f'کد ملی {s_nid} ({s_name}) در فرم تکراری وارد شده است.'}, status=status.HTTP_400_BAD_REQUEST)
                if s_phone in seen_phones:
                    return Response({'error': f'شماره موبایل {s_phone} ({s_name}) در فرم تکراری وارد شده است.'}, status=status.HTTP_400_BAD_REQUEST)

                # تکراری بودن در کل دیتابیس
                if User.objects.filter(Q(national_id=s_nid) | Q(username=s_nid)).exists():
                    return Response({'error': f'دانش‌آموزی با کد ملی {s_nid} ({s_name}) قبلاً در سامانه ثبت شده است.'}, status=status.HTTP_400_BAD_REQUEST)
                if User.objects.filter(phone_number=s_phone).exists():
                    return Response({'error': f'شماره موبایل {s_phone} ({s_name}) قبلاً در سامانه ثبت شده است.'}, status=status.HTTP_400_BAD_REQUEST)

            seen_nids.add(s_nid)
            seen_phones.add(s_phone)

        # ۳. اعتبارسنجی مقادیر مدرسه
        g_name = str(group_data.get('group_name', '')).strip()
        g_prov = str(group_data.get('province', '')).strip()
        g_city = str(group_data.get('city', '')).strip()
        g_school = str(group_data.get('school_name', '')).strip()
        g_phone = str(group_data.get('school_phone', '')).strip()

        if not g_name or not g_school:
            return Response({'error': 'نام گروه و نام مدرسه الزامی است.'}, status=status.HTTP_400_BAD_REQUEST)

        # ----------------------------------------------------
        # فاز ۲: ذخیره‌سازی قطعی و یکپارچه در دیتابیس
        # ----------------------------------------------------
        with transaction.atomic():
            if is_new_leader:
                leader_user = User.objects.create_user(
                    username=l_nid,
                    national_id=l_nid,
                    email=l_email,
                    password=l_password,
                    first_name=l_first_name,
                    last_name=l_last_name,
                    phone_number=l_phone,
                    role='normal'
                )

            group = SchoolGroup.objects.create(
                group_name=g_name,
                province=g_prov,
                city=g_city,
                school_name=g_school,
                school_phone=g_phone,
                organizer=leader_user,
                finalized=True
            )

            for idx, s in enumerate(students_data):
                s_nid = str(s.get('national_id', '')).strip()
                s_first = str(s.get('first_name', '')).strip()
                s_last = str(s.get('last_name', '')).strip()
                s_phone = str(s.get('phone_number', '')).strip()
                s_grade = str(s.get('grade', '')).strip()
                s_major = str(s.get('major', '')).strip()

                is_leader = (idx == 0 or s_nid == l_nid)
                if is_leader:
                    u = leader_user
                    if s_first: u.first_name = s_first
                    if s_last: u.last_name = s_last
                    if s_phone: u.phone_number = s_phone
                    u.save()
                else:
                    fake_email = f"{s_nid}@example.com"
                    u = User.objects.create_user(
                        username=s_nid,
                        national_id=s_nid,
                        email=fake_email,
                        password=s_nid,
                        first_name=s_first,
                        last_name=s_last,
                        phone_number=s_phone,
                        role='normal'
                    )

                Student.objects.create(
                    user=u,
                    school_group=group,
                    grade=s_grade,
                    major=s_major
                )

        refresh = RefreshToken.for_user(leader_user)
        return Response({
            'success': True,
            'groupId': group.id,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': leader_user.id,
                'email': leader_user.email,
                'username': leader_user.username,
                'national_id': leader_user.national_id,
                'first_name': leader_user.first_name,
                'last_name': leader_user.last_name,
                'role': leader_user.role
            }
        }, status=status.HTTP_201_CREATED)
