from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied


ROLE_VIEWER = 'Viewer'
ROLE_VENDOR = 'Vendor'
ROLE_HOST = 'Host'
ROLE_DEVELOPER = 'Developer'
ROLE_ADMIN = 'Admin'

VENDOR_GROUPS = {ROLE_VENDOR, ROLE_HOST}
DEVELOPER_GROUPS = {ROLE_DEVELOPER, ROLE_ADMIN}


def assign_role(user, role_name):
    group, _ = Group.objects.get_or_create(name=role_name)
    user.groups.add(group)


def user_group_names(user):
    if not user.is_authenticated:
        return set()
    return set(user.groups.values_list('name', flat=True))


def is_vendor(user):
    return bool(VENDOR_GROUPS & user_group_names(user))


def is_developer(user):
    if user.is_staff or user.is_superuser:
        return True
    return bool(DEVELOPER_GROUPS & user_group_names(user))


def vendor_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not is_vendor(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapped


def developer_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not is_developer(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapped
