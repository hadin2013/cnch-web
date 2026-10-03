from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class NationalIdOrEmailBackend(ModelBackend):
    """
    امکان ورود کاربران با کد ملی یا ایمیل به عنوان نام کاربری
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if not username or not password:
            return None
        username = str(username).strip()
        try:
            user = User.objects.filter(
                Q(username__iexact=username) |
                Q(national_id__iexact=username) |
                Q(email__iexact=username)
            ).first()
            if user and user.check_password(password):
                return user
        except Exception:
            return None
        return None
