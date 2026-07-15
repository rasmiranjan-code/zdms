# apps/core/context_processors.py

def notification_context(request):
    if request.user.is_authenticated:
        return {
            'unread_notification_count': 0,
        }
    return {}