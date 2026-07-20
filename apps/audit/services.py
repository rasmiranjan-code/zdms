# apps/audit/services.py
from django.contrib.contenttypes.models import ContentType
from .models import AuditLog

def log_action(actor=None, action="", target=None):
    """
    Creates an audit log entry in the database.
    """
    log_entry = AuditLog(actor=actor, action=action)
    if target:
        log_entry.target_content_type = ContentType.objects.get_for_model(target)
        log_entry.target_object_id = target.pk
    log_entry.save()
    print(f"[AUDIT] Actor={actor} Action={action} Target={target}")