from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# =========================
# ПРОФИЛЬ + РОЛИ
# =========================

class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('teacher', 'Учитель'),
        ('director', 'Директор'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# =========================
# ЗАЯВКИ
# =========================

class Application(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    course = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} — {self.course}"


# =========================
# КУРСЫ И УРОКИ
# =========================

class Course(models.Model):
    LEVELS = (
        ("BEG", "Beginner"),
        ("MID", "Middle"),
        ("PRO", "Pro"),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    level = models.CharField(max_length=3, choices=LEVELS, default="BEG")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cover = models.ImageField(upload_to="course_covers/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        related_name="lessons",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    video_url = models.URLField(blank=True, null=True)
    content = models.TextField(blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} — {self.title}"


# =========================
# ЗАПИСЬ НА КУРС
# =========================

class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="enrollments",
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course,
        related_name="enrollments",
        on_delete=models.CASCADE
    )
    active = models.BooleanField(default=True)
    purchased_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student.username} -> {self.course.title}"


class Certificate(models.Model):
    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="certificate"
    )
    issued_at = models.DateTimeField(auto_now_add=True)
    cert_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Certificate {self.cert_number}"


# =========================
# ПРОФИЛИ УЧИТЕЛЯ И ДИРЕКТОРА
# =========================

class TeacherProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Teacher: {self.user.username}"


class DirectorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='director_profile'
    )
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Director: {self.user.username}"


# =========================
# ГРУППЫ СТУДЕНТОВ
# =========================

class StudentGroup(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        related_name='groups'
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='student_groups'  # ✅ ИСПРАВЛЕНО
    )

    def __str__(self):
        return f"{self.name} — {self.teacher.user.username}"


# =========================
# ЖУРНАЛ ОЦЕНОК
# =========================

class JournalEntry(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='journal_entries'
    )
    group = models.ForeignKey(
        StudentGroup,
        on_delete=models.CASCADE,
        related_name='journal_entries'
    )
    date = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=5)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.username} — {self.grade}"


# =========================
# ВИДЕОУРОКИ
# =========================

class VideoLesson(models.Model):
    course = models.ForeignKey(
        Course,
        related_name='videos',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='video_lessons/')
    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
