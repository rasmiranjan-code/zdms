# apps/core/validators.py

import re
from django.core.exceptions import ValidationError


def validate_roll_number(value):
    if not re.match(r'^[A-Za-z0-9\-\/]+$', value):
        raise ValidationError('Invalid roll number format.')


def validate_file_size(file, max_mb=10):
    limit = max_mb * 1024 * 1024
    if file.size > limit:
        raise ValidationError(f'File size must not exceed {max_mb}MB.')


def validate_file_type(file, allowed_extensions):
    ext = file.name.split('.')[-1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(f'Unsupported file type: .{ext}')