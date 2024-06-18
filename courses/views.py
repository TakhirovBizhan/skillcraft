from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, CourseStep, Enrollment, Progress
from .forms import CourseForm, CourseStepForm
from notes.models import Note

@login_required
def step_detail(request, step_id):
    step = get_object_or_404(CourseStep, id=step_id)
    course = step.course
    is_author = course.is_author(request.user)
    is_completed = Progress.objects.filter(user=request.user, step=step, completed=True).exists()
    
    return render(request, 'courses/step_detail.html', {
        'step': step,
        'course': course,
        'is_author': is_author,
        'is_completed': is_completed,
    })

@login_required
def complete_step(request, step_id):
    step = get_object_or_404(CourseStep, id=step_id)
    course = step.course
    progress, created = Progress.objects.get_or_create(user=request.user, step=step, defaults={'course': course})
    progress.completed = True
    progress.save()
    return redirect('course_detail', course_id=course.id)

@login_required
def course_list(request):
    courses = Course.objects.all()
    enrollments = Enrollment.objects.filter(user=request.user).values_list('course_id', flat=True)
    notes = Note.objects.filter(user=request.user).values_list('course_id', flat=True)
    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'enrollments': enrollments,
        'notes': notes
    })

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    steps = course.steps.all()
    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    progress = Progress.objects.filter(user=request.user, step__in=steps, completed=True).values_list('step_id', flat=True)

    total_steps = steps.count()
    completed_steps = progress.count()
    is_author = course.is_author(request.user)

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'steps': steps,
        'is_enrolled': is_enrolled,
        'progress': progress,
        'total_steps': total_steps,
        'completed_steps': completed_steps,
        'is_author': is_author,
    })

@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not course.is_author(request.user):
        return redirect('course_detail', course_id=course.id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.is_author(request.user):
        course.delete()
    return redirect('course_list')

@login_required
def add_step(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not course.is_author(request.user):
        return redirect('course_detail', course_id=course.id)
    if request.method == 'POST':
        form = CourseStepForm(request.POST)
        if form.is_valid():
            step = form.save(commit=False)
            step.course = course
            step.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseStepForm()
    return render(request, 'courses/step_form.html', {'form': form, 'course': course})

@login_required
def edit_step(request, course_id, step_id):
    step = get_object_or_404(CourseStep, id=step_id, course_id=course_id)
    course = step.course
    if not course.is_author(request.user):
        return redirect('course_detail', course_id=course.id)
    if request.method == 'POST':
        form = CourseStepForm(request.POST, instance=step)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseStepForm(instance=step)
    return render(request, 'courses/step_form.html', {'form': form, 'course': course})

@login_required
def delete_step(request, course_id, step_id):
    step = get_object_or_404(CourseStep, id=step_id, course_id=course_id)
    course = step.course
    if course.is_author(request.user):
        step.delete()
    return redirect('course_detail', course_id=course.id)

@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('course_detail', course_id=course.id)

@login_required
def unenroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.filter(user=request.user, course=course).delete()
    return redirect('profile')

@login_required
def mark_step_complete(request, step_id):
    step = get_object_or_404(CourseStep, id=step_id)
    progress, created = Progress.objects.get_or_create(user=request.user, step=step, course=step.course)
    progress.completed = True
    progress.save()
    return redirect('course_detail', course_id=step.course.id)