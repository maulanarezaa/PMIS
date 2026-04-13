from django.http import HttpResponseForbidden
from viewsPermission import user_has_permission

def permission_required(kode_permission):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not user_has_permission(request.user, kode_permission):
                return HttpResponseForbidden("Tidak punya akses")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator