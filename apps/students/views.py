from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from apps.academics.models import Enrollment, Subject, Batch, Semester
from apps.accounts.models import FacultySubjectBatchMapping, User
from django.db.models import Count, Q
from apps.accounts.models import User
from apps.core.decorators import hod_required
from apps.core.mixins import HODRequiredMixin
from django.shortcuts import get_object_or_404 
from apps.accounts.forms import StudentUpdateForm

from apps.attendance.models import Attendance

@hod_required
def student_list(request):
    # Get filter parameters from the request
    batch_id = request.GET.get('batch')
    semester_id = request.GET.get('semester')

    # Base queryset for active enrollments
    enrollments = Enrollment.objects.filter(is_active=True, student__role='STUDENT').select_related(
        'student__studentprofile', 'batch__academic_session', 'current_semester'
    ).order_by('student__first_name', 'student__last_name')

    # Apply filters if they are provided
    if batch_id:
        enrollments = enrollments.filter(batch_id=batch_id)
    if semester_id:
        enrollments = enrollments.filter(current_semester_id=semester_id)

    # Data for filter dropdowns
    all_batches = Batch.objects.all().select_related('academic_session').order_by('-academic_session__start_year')
    all_semesters = Semester.objects.all().order_by('number')

    context = {
        'enrollments': enrollments,
        'all_batches': all_batches,
        'all_semesters': all_semesters,
        'selected_batch': int(batch_id) if batch_id else None,
        'selected_semester': int(semester_id) if semester_id else None,
    }
    return render(request, "students/list.html", context)

@hod_required
def student_detail(request, pk):
    student = get_object_or_404(User, pk=pk, role='STUDENT')
    enrollment = Enrollment.objects.filter(student=student, is_active=True).first()
    context = {'student': student, 'enrollment': enrollment}
    return render(request, 'students/detail.html', context)

class StudentUpdateView(HODRequiredMixin, UpdateView):
    model = User
    form_class = StudentUpdateForm
    template_name = 'students/edit.html'
    
    def get_success_url(self):
        return reverse_lazy('students:detail', kwargs={'pk': self.object.pk})

@login_required
def dashboard(request):
    student = request.user
    try:
        enrollment = Enrollment.objects.select_related('batch', 'current_semester').get(student=student, is_active=True)
    except Enrollment.DoesNotExist:
        enrollment = None
    context = {'enrollment': enrollment}
    return render(request, "students/dashboard.html", context)


@login_required
def attendance_view(request):
    student = request.user
    attendance_records = []
    total_attended = 0
    total_classes = 0

    try:
        # Find the student's current enrollment and subjects
        enrollment = Enrollment.objects.get(student=student, is_active=True)
        subjects = enrollment.current_semester.subjects.all()

        for subject in subjects:
            # Get attendance stats for each subject
            stats = Attendance.objects.filter(
                student=student, subject=subject
            ).aggregate(
                total=Count('id'),
                attended=Count('id', filter=Q(is_present=True))
            )

            subject_total = stats.get('total', 0)
            subject_attended = stats.get('attended', 0)

            percentage = (subject_attended / subject_total * 100) if subject_total > 0 else 0

            attendance_records.append({
                'subject': subject.name,
                'total': subject_total,
                'attended': subject_attended,
                'percentage': percentage,
            })
            total_classes += subject_total
            total_attended += subject_attended

    except Enrollment.DoesNotExist:
        pass

    overall_percentage = (total_attended / total_classes * 100) if total_classes > 0 else 0

    context = {
        'attendance_records': attendance_records,
        'overall_percentage': overall_percentage,
    }
    return render(request, "students/attendance.html", context)

def my_faculty_view(request):
    student = request.user
    assignments = []
    current_semester = None
    try:
        enrollment = Enrollment.objects.get(student=student, is_active=True)
        current_semester = enrollment.current_semester
        # Find subjects for the student's current semester
        subjects = current_semester.subjects.all()
        # Find faculty assignments for those subjects
        assignments = FacultySubjectBatchMapping.objects.filter(
            subject__in=subjects
        ).select_related('faculty', 'subject').order_by('subject__name')
    except Enrollment.DoesNotExist:
        pass # Handle case where student has no active enrollment

    context = {
        'assignments': assignments,
        'current_semester': current_semester,
    }
    return render(request, 'students/my_faculty.html', context)