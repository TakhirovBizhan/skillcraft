from django.db import models
from django.contrib.auth.models import User
from courses.models import Course, CourseStep

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='notes')

    def __str__(self):
        return f"Note by {self.user.username} on {self.course.title}"
