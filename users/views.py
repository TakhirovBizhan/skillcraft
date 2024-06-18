from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm  # Импортируем нашу кастомную форму
from courses.models import Course, Enrollment

def home(request):
    if request.user.is_authenticated:
        return redirect('course_list')  # Или на любую другую страницу для аутентифицированных пользователей
    else:
        return redirect('login')  # Или 'register' если хотите перенаправлять на регистрацию

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    created_courses = Course.objects.filter(user=request.user)
    enrolled_courses = Enrollment.objects.filter(user=request.user).select_related('course')
    return render(request, 'profile.html', {  # Обновляем путь к шаблону
        'created_courses': created_courses,
        'enrolled_courses': enrolled_courses,
    })
