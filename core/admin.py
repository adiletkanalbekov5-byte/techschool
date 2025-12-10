# core/admin.py
from django.contrib import admin
from .models import( Course,
    Enrollment, Lesson,
    Certificate,    TeacherProfile,
    DirectorProfile,StudentGroup,
    JournalEntry,VideoLesson,
)
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title","level","price","created_at")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title","course","order")

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student","course","active","purchased_at")

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("cert_number","enrollment","issued_at")

# --- Профили ---
@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'bio')
    search_fields = ('user__username', 'phone')

@admin.register(DirectorProfile)
class DirectorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'phone')

# --- Группы студентов ---
@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')
    filter_horizontal = ('students',)

# --- Журнал ---
@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('student', 'group', 'date', 'grade')
    list_filter = ('group', 'date')
    search_fields = ('student__username', 'group__name')

# --- Видео уроки ---
@admin.register(VideoLesson)
class VideoLessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'teacher', 'created_at')
    list_filter = ('course', 'teacher')
    search_fields = ('title',)

