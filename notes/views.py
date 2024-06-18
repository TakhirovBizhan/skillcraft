from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Note
from courses.models import Course

@login_required
def note_list(request):
    notes = request.user.notes.all()
    return render(request, 'notes/note_list.html', {'notes': notes})

@login_required
def add_note(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Note.objects.get_or_create(user=request.user, course=course)
    return redirect('note_list')

@login_required
def remove_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    return redirect('note_list')