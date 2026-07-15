# apps/core/utils.py

from django.utils import timezone


def current_academic_year():
    now = timezone.now()
    return now.year if now.month >= 6 else now.year - 1


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')