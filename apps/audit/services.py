# apps/audit/services.py

def log_action(actor=None, action="", target=None):
    """
    Temporary audit logger.
    Later this can save logs to the database.
    """
    print(
        f"[AUDIT] Actor={actor} Action={action} Target={target}"
    )