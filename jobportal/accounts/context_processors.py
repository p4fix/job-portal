from .models import Profile


def user_role(request):
    """Provide user_role in template context; None if not authenticated or no profile."""
    if not request.user.is_authenticated:
        return {'user_role': None}
    try:
        return {'user_role': request.user.profile.role}
    except Profile.DoesNotExist:
        return {'user_role': None}
