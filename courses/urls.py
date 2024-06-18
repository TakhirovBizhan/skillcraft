from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('create/', views.create_course, name='create_course'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('<int:course_id>/add_step/', views.add_step, name='add_step'),
    path('<int:course_id>/step/<int:step_id>/edit/', views.edit_step, name='edit_step'),
    path('<int:course_id>/step/<int:step_id>/delete/', views.delete_step, name='delete_step'),
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),
    path('<int:course_id>/unenroll/', views.unenroll, name='unenroll'),
    path('step/<int:step_id>/complete/', views.mark_step_complete, name='mark_step_complete'),
    path('<int:step_id>/complete/', views.complete_step, name='complete_step'),
    path('step/complete/<int:step_id>/', views.complete_step, name='complete_step'),
    path('courses/steps/<int:step_id>/', views.step_detail, name='step_detail'), 
]