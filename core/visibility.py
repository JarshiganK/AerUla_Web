"""Public surface visibility gates (respects SiteViewerSettings; platform operators bypass)."""

from django.shortcuts import render

from accounts.roles import is_developer

from .models import SiteViewerSettings


def viewer_surface_allowed(request, attribute_name):
    """attribute_name matches a BooleanField on SiteViewerSettings."""
    if request.user.is_authenticated and is_developer(request.user):
        return True
    return getattr(SiteViewerSettings.get_solo(), attribute_name)


def public_unavailable(request, *, headline=None):
    """Soft gate: 200 OK with explanatory copy (operators still use bypass in views)."""
    return render(
        request,
        'core/public_unavailable.html',
        {
            'unavailable_headline': headline or 'This area is not available right now.',
        },
        status=200,
    )


def guard_viewer_surface(request, attribute_name):
    """
    Returns None if the surface is allowed, otherwise an HttpResponse
    rendered for public viewers.
    """
    if viewer_surface_allowed(request, attribute_name):
        return None
    return public_unavailable(request)
