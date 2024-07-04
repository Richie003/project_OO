from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def noCategory(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.category == 'None' and request.META['HTTP_REFERER'] == 'http://127.0.0.1:8001/user/account/login/':
            return redirect('category')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.category:
                group = request.user.category
                print(group)
            if request.user.category != '':
                for roles in allowed_roles:
                    if group == roles:
                        return view_func(request, *args, **kwargs)
                    else:
                        try:
                            path = request.META['HTTP_REFERER']
                            # print(path)
                            return redirect(path)
                        except:
                            return redirect('/')
            else:
                return view_func(request, *args, **kwargs)

        return wrapper_func

    return decorator


# def link(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         if vars == True:
#             return redirect('download')
#         return view_func(request, *args, **kwargs)

#     return wrapper_func


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

            if group == 'user':
                return redirect('index')

            if group == 'admin':
                return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('you are not allowed')

    return wrapper_function
