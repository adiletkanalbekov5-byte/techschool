from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import (
    Course, Lesson, Enrollment, Certificate,
    TeacherProfile, DirectorProfile,
    StudentGroup, JournalEntry, VideoLesson,
    Application
)

from .serializers import (
    CourseListSerializer, CourseDetailSerializer,
    LessonSerializer, EnrollmentSerializer, CertificateSerializer,
    TeacherProfileSerializer, DirectorProfileSerializer,
    StudentGroupSerializer, JournalEntrySerializer,
    VideoLessonSerializer, UserSerializer, ApplicationSerializer
)

# =========================
# PERMISSIONS
# =========================

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.role == 'teacher'
        )


class IsDirector(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.role == 'director'
        )


# =========================
# ADMIN
# =========================

class AdminApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.order_by('-created_at')
    serializer_class = ApplicationSerializer
    permission_classes = [IsAdmin]


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


# =========================
# COURSES
# =========================

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().prefetch_related("lessons")
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        return CourseListSerializer if self.action == "list" else CourseDetailSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# =========================
# ENROLLMENTS
# =========================

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Enrollment.objects.all()
        return Enrollment.objects.filter(student=user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


# =========================
# CERTIFICATES
# =========================

class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Certificate.objects.select_related(
        "enrollment__student",
        "enrollment__course"
    )
    serializer_class = CertificateSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["get"], url_path="by-number")
    def by_number(self, request):
        num = request.query_params.get("q")
        if not num:
            return Response(
                {"detail": "provide ?q=cert_number"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cert = self.queryset.filter(cert_number=num).first()
        if not cert:
            return Response(
                {"detail": "not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(self.get_serializer(cert).data)


# =========================
# TEACHER / DIRECTOR PROFILES
# =========================

class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAdmin | IsTeacher]


class DirectorProfileViewSet(viewsets.ModelViewSet):
    queryset = DirectorProfile.objects.all()
    serializer_class = DirectorProfileSerializer
    permission_classes = [IsAdmin | IsDirector]


# =========================
# STUDENT GROUPS
# =========================

class StudentGroupViewSet(viewsets.ModelViewSet):
    serializer_class = StudentGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return StudentGroup.objects.all()

        if hasattr(user, 'teacher_profile'):
            return StudentGroup.objects.filter(teacher=user.teacher_profile)

        return StudentGroup.objects.none()


# =========================
# JOURNAL (ОЦЕНКИ)
# =========================

class JournalEntryViewSet(viewsets.ModelViewSet):
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return JournalEntry.objects.filter(
            group__teacher=self.request.user.teacher_profile
        )


# =========================
# VIDEO LESSONS
# =========================

class VideoLessonViewSet(viewsets.ModelViewSet):
    queryset = VideoLesson.objects.all()
    serializer_class = VideoLessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'teacher_profile'):
            raise permissions.PermissionDenied("Only teachers can upload videos")

        serializer.save(teacher=self.request.user.teacher_profile)
