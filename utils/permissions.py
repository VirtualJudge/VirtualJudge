from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet


def check_permissions(*permissions):
    """
    检查是否包含一些权限，
    权限列表为空的情况下相当于isAuthenticated。
    request.user.is_staff是的话，默认通过
    :return: function
    """

    def decorator(func):
        def wrapper(view: ViewSet, request: Request, *args, **kw):
            if request.user.is_anonymous:
                raise NotAuthenticated
            if request.user.is_staff or request.user.has_perms(perm_list=permissions):
                return func(view, request, *args, **kw)
            else:
                raise PermissionDenied

        return wrapper

    return decorator


def is_authenticated():
    """
    :return: function
    """

    def decorator(func):
        def wrapper(view: ViewSet, request: Request, *args, **kw):
            if request.user.is_anonymous:
                raise NotAuthenticated
            return func(view, request, *args, **kw)

        return wrapper

    return decorator


def is_administrator():
    """
    :return: function
    """

    def decorator(func):
        def wrapper(view: ViewSet, request: Request, *args, **kw):
            if request.user.is_staff:
                return func(view, request, *args, **kw)
            raise NotAuthenticated

        return wrapper

    return decorator
