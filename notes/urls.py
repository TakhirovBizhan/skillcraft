from django.urls import path
from . import views

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('add/<int:course_id>/', views.add_note, name='add_note'),
    path('remove/<int:note_id>/', views.remove_note, name='remove_note'),
]