from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            if request.user.role != role and request.user.role != 'admin':
                # admin اجازهٔ دسترسی عمومی دارد
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator

# چنانچه می‌خواهی برای چند نقش مجاز باشه:
def roles_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            if request.user.role not in roles and request.user.role != 'admin':
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
