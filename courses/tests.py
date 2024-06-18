from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Course, CourseStep, Enrollment, Progress

class CourseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.course = Course.objects.create(title='Test Course', description='Course description', user=self.user)

    def test_course_creation(self):
        self.assertEqual(self.course.title, 'Test Course')
        self.assertEqual(self.course.description, 'Course description')
        self.assertEqual(self.course.user, self.user)

class CourseStepModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.course = Course.objects.create(title='Test Course', description='Course description', user=self.user)
        self.step = CourseStep.objects.create(title='Test Step', description='Step description', course=self.course, article='Article text', reading_time=10)

    def test_step_creation(self):
        self.assertEqual(self.step.title, 'Test Step')
        self.assertEqual(self.step.course, self.course)

class EnrollmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.course = Course.objects.create(title='Test Course', description='Course description', user=self.user)
        self.enrollment = Enrollment.objects.create(user=self.user, course=self.course)

    def test_enrollment_creation(self):
        self.assertEqual(self.enrollment.user, self.user)
        self.assertEqual(self.enrollment.course, self.course)

class ProgressModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.course = Course.objects.create(title='Test Course', description='Course description', user=self.user)
        self.step = CourseStep.objects.create(title='Test Step', description='Step description', course=self.course, article='Article text', reading_time=10)
        self.progress = Progress.objects.create(user=self.user, course=self.course, step=self.step, completed=True)

    def test_progress_creation(self):
        self.assertEqual(self.progress.user, self.user)
        self.assertEqual(self.progress.course, self.course)
        self.assertEqual(self.progress.step, self.step)
        self.assertTrue(self.progress.completed)

class CourseViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.course = Course.objects.create(title='Test Course', description='Course description', user=self.user)

    def test_course_list_view(self):
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_list.html')

    def test_course_detail_view(self):
        response = self.client.get(reverse('course_detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_detail.html')

    def test_enroll_view(self):
        response = self.client.post(reverse('enroll', args=[self.course.id]))
        self.assertRedirects(response, reverse('course_detail', args=[self.course.id]))
        self.assertTrue(Enrollment.objects.filter(user=self.user, course=self.course).exists())

class CourseStepViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.course = Course.objects.create(title='Test Course', description='Course description', user=self.user)
        self.step = CourseStep.objects.create(title='Test Step', description='Step description', course=self.course, article='Article text', reading_time=10)

    def test_step_detail_view(self):
        response = self.client.get(reverse('step_detail', args=[self.step.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/step_detail.html')

    def test_complete_step_view(self):
        response = self.client.post(reverse('complete_step', args=[self.step.id]))
        self.assertRedirects(response, reverse('course_detail', args=[self.course.id]))
        self.assertTrue(Progress.objects.filter(user=self.user, step=self.step, completed=True).exists())
