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


def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.exists():
                user_groups = set(group.name for group in request.user.groups.all())  # Get all group names
                allowed_roles_set = set(allowed_roles)  # Convert allowed roles to a set for efficient lookup
                
                if user_groups & allowed_roles_set:  # Check if there is any common group
                    return view_func(request, *args, **kwargs)  # Allow access
            
            return HttpResponse('You are not authorized to view this page.', status=403)  # Forbidden response
        
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