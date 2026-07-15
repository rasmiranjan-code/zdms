# apps/accounts/permissions.py

def is_hod(user):
    return user.is_authenticated and user.role == 'HOD'


def is_faculty(user):
    return user.is_authenticated and user.role in ('FACULTY', 'HOD')


def is_student(user):
    return user.is_authenticated and user.role == 'STUDENT'


def can_create_student(user):
    return user.is_authenticated and user.role in ('FACULTY', 'HOD')


def can_create_faculty(user):
    return user.is_authenticated and user.role == 'HOD'