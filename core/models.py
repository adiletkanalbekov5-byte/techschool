# core/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

User = get_user_model()

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    course = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} — {self.course}"

class Course(models.Model):
    LEVELS = (("BEG","Beginner"), ("MID","Middle"), ("PRO","Pro"))
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    level = models.CharField(max_length=3, choices=LEVELS, default="BEG")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to="course_covers/", null=True, blank=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    video_url = models.URLField(blank=True, null=True)  # можно хранить ссылку на HLS/Vimeo
    content = models.TextField(blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} — {self.title}"

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="enrollments", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="enrollments", on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    purchased_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student} -> {self.course}"

class Certificate(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name="certificate")
    issued_at = models.DateTimeField(auto_now_add=True)
    cert_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Cert {self.cert_number} for {self.enrollment}"

User = settings.AUTH_USER_MODEL

# Профиль учителя
class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'Teacher: {self.user.username}'

# Профиль директора
class DirectorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='director_profile')
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'Director: {self.user.username}'

# Группы учеников
class StudentGroup(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='groups')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='student_groups')

    def __str__(self):
        return f'{self.name} ({self.teacher.user.username})'


# Журнал посещаемости/оценок (для простоты)
class JournalEntry(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=5, blank=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f'{self.student.username} - {self.group.name} - {self.date}'

# Видеоуроки (для курсов)
class VideoLesson(models.Model):
    course = models.ForeignKey('Course', related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='video_lessons/')
    created_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.title} ({self.course.title})'