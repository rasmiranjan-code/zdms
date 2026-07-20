# apps/accounts/signals.py

from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from apps.accounts.models import User


@receiver(post_save, sender=User)
def log_and_notify_on_creation(sender, instance, created, **kwargs):
    if created:
        from apps.audit.services import log_action
        log_action(
            actor=instance.created_by,
            action=f'CREATED_{instance.role}_ACCOUNT',
            target=instance,
        )
        if instance.role == 'STUDENT':
            pass  # HOD notify hook here later

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    from apps.audit.services import log_action
    log_action(actor=user, action='USER_LOGGED_IN')