from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect ('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

# def allowed_user(allowed_roles=[]):
#     def decorator(view_func):
#         @wraps(view_func)
#         def wrapper_func(request, *args, **kwargs):
#             group = None
#             if request.user.groups.exists():
#                 group = request.user.groups.all()[0].name  # Get the first group name

#             if group in allowed_roles:
#                 return view_func(request, *args, **kwargs)  # Allow access
            
#             return HttpResponse('You are not authorized to view this page.', status=403)  # Forbidden response
        
#         return wrapper_func
#     return decorator

def allowed_user(*allowed_roles):  # ✅ Accept multiple roles as separate arguments
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.exists():
                user_groups = {group.name for group in request.user.groups.all()}
                print(f"🔍 Debugging Allowed User Decorator:")
                print(f"👤 User: {request.user.username}")
                print(f"👥 User Groups: {user_groups}")
                print(f"✅ Allowed Roles: {allowed_roles}")
                if user_groups.intersection(allowed_roles):  # ✅ Check if user has any allowed role
                    return view_func(request, *args, **kwargs)  # ✅ Grant access
            
            return HttpResponse('You are not authorized to view this page.', status=403)  # ❌ Forbidden response
        
        return wrapper_func
    return decorator



def admissions_only(view_func):
    def wrapper_func(request, *arges, **kwargs):
        group=None
        if request.user.groups.exists():
            group - request.user.groups.all()[0].name
        if group == 'student':
            return redirect(homepage)
        if group == 'admissions':
            return view_func(request, *args, **kwargs)
    return wrapper_func