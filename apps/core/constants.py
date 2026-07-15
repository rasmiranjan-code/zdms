# apps/core/constants.py

GRADE_SCALE_DEFAULT = [
    ('O', 10, 90, 100),
    ('A+', 9, 80, 89),
    ('A', 8, 70, 79),
    ('B+', 7, 60, 69),
    ('B', 6, 50, 59),
    ('C', 5, 40, 49),
    ('F', 0, 0, 39),
]

RESULT_STATUS_CHOICES = (
    ('DRAFT', 'Draft'),
    ('REVIEW', 'Under Review'),
    ('PUBLISHED', 'Published'),
)

SEMESTER_STATUS_CHOICES = (
    ('UPCOMING', 'Upcoming'),
    ('ACTIVE', 'Active'),
    ('COMPLETED', 'Completed'),
    ('LOCKED', 'Locked'),
)

ROLE_CHOICES = (
    ('HOD', 'HOD'),
    ('FACULTY', 'Faculty'),
    ('STUDENT', 'Student'),
)

SUBJECT_TYPE_CHOICES = (
    ('THEORY', 'Theory'),
    ('PRACTICAL', 'Practical'),
    ('ELECTIVE', 'Elective'),
)