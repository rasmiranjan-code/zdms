# apps/accounts/signals.py

from django.db.models.signals import post_save
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