from rest_framework import serializers
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import SchoolGroup, Student, Ticket

User = get_user_model()

class SchoolGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolGroup
        fields = ['id','group_name','province','city','school_name','school_phone']

class StudentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    national_id = serializers.CharField(max_length=10)
    phone_number = serializers.CharField(max_length=20)

    class Meta:
        model = Student
        fields = ["school_group","first_name","last_name","national_id","phone_number","grade","major"]

    def validate(self, attrs):
        group = attrs["school_group"]
        request = self.context.get("request")
        if group.students.count() >= 6:
            raise serializers.ValidationError({"school_group": "این گروه به حداکثر ظرفیت (۶ دانش‌آموز) رسیده است."})
        
        user_by_nid = User.objects.filter(national_id=attrs.get("national_id")).first()
        user_by_phone = User.objects.filter(phone_number=attrs.get("phone_number")).first()

        # بررسی اینکه آیا این رکورد متعلق به سرگروه لاگین‌شده است یا خیر
        is_organizer = bool(
            request and request.user.is_authenticated and (
                request.user == user_by_nid or
                request.user == user_by_phone or
                (request.user.national_id and request.user.national_id == attrs.get("national_id")) or
                (request.user.phone_number and request.user.phone_number == attrs.get("phone_number"))
            )
        )

        if not is_organizer:
            if user_by_phone:
                raise serializers.ValidationError({"phone_number": "کاربری با این تلفن همراه قبلاً ثبت شده است."})
            if user_by_nid:
                raise serializers.ValidationError({"national_id": "کاربری با این کد ملی قبلاً ثبت شده است."})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user_data = {
            "first_name": validated_data.pop("first_name"),
            "last_name": validated_data.pop("last_name"),
            "national_id": validated_data.pop("national_id"),
            "phone_number": validated_data.pop("phone_number"),
        }
        national_id = user_data["national_id"]
        request = self.context.get("request")
        group = validated_data.get("school_group")

        user_by_nid = User.objects.filter(national_id=national_id).first()
        user_by_phone = User.objects.filter(phone_number=user_data["phone_number"]).first()

        is_organizer = bool(
            request and request.user.is_authenticated and (
                request.user == user_by_nid or
                request.user == user_by_phone or
                (request.user.national_id and request.user.national_id == national_id) or
                (request.user.phone_number and request.user.phone_number == user_data["phone_number"])
            )
        )

        if is_organizer:
            user = request.user
            for k, v in user_data.items():
                if v:
                    setattr(user, k, v)
            user.save()
            student, _ = Student.objects.update_or_create(
                user=user,
                defaults={
                    "school_group": group,
                    "grade": validated_data.get("grade"),
                    "major": validated_data.get("major"),
                }
            )
        else:
            email = f"{national_id}@example.com"
            user = User.objects.create_user(
                username=national_id,
                email=email,
                password=national_id,
                **user_data
            )
            student = Student.objects.create(user=user, **validated_data)
        return student
    
    @transaction.atomic
    def update(self, instance, validated_data):
        user = instance.user
        for field in ["first_name", "last_name", "national_id", "phone_number"]:
            if field in validated_data:
                setattr(user, field, validated_data.pop(field))
        user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        return {
            "id": instance.user.id,
            "school_group": instance.school_group.id,
            "first_name": instance.user.first_name,
            "last_name": instance.user.last_name,
            "national_id": instance.user.national_id,
            "phone_number": instance.user.phone_number,
            "grade": instance.grade,
            "major": instance.major,
        }


class StudentListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    national_id = serializers.CharField(source="user.national_id")
    phone_number = serializers.CharField(source="user.phone_number")

    class Meta:
        model = Student
        fields = ['user','first_name','last_name','national_id','phone_number','grade','major']

class SchoolGroupDashboardSerializer(serializers.ModelSerializer):
    students = StudentListSerializer(many=True, read_only=True)

    class Meta:
        model = SchoolGroup
        fields = ['id','group_name','province','city','school_name','school_phone','students',]


# ---------------------------------------------------------------------------
# Profile / Auth serializers
# ---------------------------------------------------------------------------

class UserSerializer(serializers.ModelSerializer):
    """The signed-in user's own profile (read + editable personal fields)."""

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'phone_number', 'national_id', 'date_of_birth', 'address',
                  'role', 'is_email_activated', 'user_credit', 'created_at']
        read_only_fields = ['id', 'username', 'national_id', 'role',
                            'is_email_activated', 'user_credit', 'created_at']

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("این ایمیل قبلاً توسط کاربر دیگری ثبت شده است.")
        return value

    def validate_phone_number(self, value):
        if not value:
            return value
        qs = User.objects.filter(phone_number=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("این تلفن همراه قبلاً توسط کاربر دیگری ثبت شده است.")
        return value

    def update(self, instance, validated_data):
        old_email = instance.email
        instance = super().update(instance, validated_data)
        if 'email' in validated_data and instance.username == old_email:
            instance.username = instance.email
            instance.save(update_fields=['username'])
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    """Signup: create an account with email + password. Username becomes the email."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(required=False, default='')
    last_name = serializers.CharField(required=False, default='')
    phone_number = serializers.CharField(required=False, allow_blank=True, default='')
    national_id = serializers.CharField(required=False, allow_blank=True, default='')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number', 'national_id']
        read_only_fields = ['id', 'username']

    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists() or \
           User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("کاربری با این ایمیل یا نام کاربری قبلاً ثبت شده است.")
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        if password and len(password) < 6:
            raise serializers.ValidationError({"password": "رمز عبور باید دست‌کم ۶ کاراکتر باشد."})
        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data.pop('password')
        phone = validated_data.pop('phone_number', '')
        national_id = validated_data.pop('national_id', '') or None
        user = User.objects.create_user(username=email, email=email, password=password,
                                        first_name=validated_data.get('first_name', ''),
                                        last_name=validated_data.get('last_name', ''))
        if phone:
            user.phone_number = phone
        if national_id:
            user.national_id = national_id
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("رمز عبور فعلی اشتباه است.")
        return value

    def validate_new_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("رمز عبور جدید باید دست‌کم ۶ کاراکتر باشد.")
        return value


# ---------------------------------------------------------------------------
# Admin serializers
# ---------------------------------------------------------------------------

class AdminUserUpdateSerializer(serializers.ModelSerializer):
    """Partial update of a user by an admin (profile fields + role)."""
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    national_id = serializers.CharField(required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number',
                  'national_id', 'date_of_birth', 'address', 'role']

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("این ایمیل قبلاً توسط کاربر دیگری ثبت شده است.")
        return value

    def validate_phone_number(self, value):
        if not value:
            return value
        qs = User.objects.filter(phone_number=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("این تلفن همراه قبلاً توسط کاربر دیگری ثبت شده است.")
        return value

    def validate_national_id(self, value):
        if not value:
            return None
        qs = User.objects.filter(national_id=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("این کد ملی قبلاً توسط کاربر دیگری ثبت شده است.")
        return value

    def update(self, instance, validated_data):
        old_email = instance.email
        instance = super().update(instance, validated_data)
        if 'email' in validated_data and instance.username == old_email:
            instance.username = instance.email
            instance.save(update_fields=['username'])
        return instance


class AdminUserRowSerializer(serializers.ModelSerializer):
    """One row of the admin's user table."""
    student_group = serializers.PrimaryKeyRelatedField(source='student_profile.school_group',
                                                       read_only=True)
    is_student = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number',
                  'national_id', 'role', 'student_group', 'is_student', 'created_at']

    def get_is_student(self, obj):
        return hasattr(obj, 'student_profile')


class RoleUpdateSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=[('normal', 'Normal User'),
                                            ('mentor', 'Mentor'),
                                            ('admin', 'Admin')])


class AdminGroupRowSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()
    organizer_name = serializers.SerializerMethodField()

    class Meta:
        model = SchoolGroup
        fields = ['id', 'group_name', 'province', 'city', 'school_name', 'school_phone',
                  'organizer', 'organizer_name', 'student_count', 'finalized']

    def get_student_count(self, obj):
        return obj.students.count()

    def get_organizer_name(self, obj):
        if obj.organizer:
            return obj.organizer.get_full_name() or obj.organizer.username
        return None


class TicketSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'user_name', 'title', 'message', 'created_at', 'resolved']
        read_only_fields = ['id', 'user', 'user_name', 'created_at', 'resolved']

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
