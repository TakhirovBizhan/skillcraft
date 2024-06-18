from django import forms
from .models import Course, CourseStep

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

class CourseStepForm(forms.ModelForm):
    class Meta:
        model = CourseStep
        fields = ['title', 'description', 'reading_time', 'article']