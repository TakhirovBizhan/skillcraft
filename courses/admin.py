from django.contrib import admin
from .models import Course, CourseStep, Enrollment, Progress, Tag

class CourseStepInline(admin.StackedInline):
    model = CourseStep
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'user', 'number_of_steps', 'created_at')
    list_filter = ('user', 'title')
    search_fields = ('title', 'description')
    inlines = [CourseStepInline]
    date_hierarchy = 'created_at'
    filter_horizontal = ('tags',)

    @admin.display(description='Number of Steps')
    def number_of_steps(self, obj):
        return obj.steps.count()

    @admin.display(description='Description')
    def short_description(self, obj):
        return obj.description[:50] 

class CourseStepAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'reading_time')
    list_filter = ('course',)
    search_fields = ('title', 'description')
    raw_id_fields = ('course',)

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')
    list_filter = ('user', 'course')
    raw_id_fields = ('user', 'course')
    search_fields = ('user__username', 'course__title')

class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'step', 'completed', 'date_completed')
    list_filter = ('user', 'course')
    search_fields = ('user__username', 'course__title', 'step__title')
    readonly_fields = ('date_completed',)

    @admin.display(description='Date Completed')
    def date_completed(self, obj):
        return obj.step.course.created_at if obj.completed else 'Not completed'

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseStep, CourseStepAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(Tag)