from django.contrib import admin
from .models import Note

class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'course_title')
    list_filter = ('user', 'course')

    def course_title(self, obj):
        return obj.course.title
    course_title.short_description = 'Course Title'

admin.site.register(Note, NoteAdmin)