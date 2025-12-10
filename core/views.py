# core/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Course, Lesson, Enrollment, Certificate,  TeacherProfile, DirectorProfile, StudentGroup, JournalEntry, VideoLesson
from .serializers import (
    CourseListSerializer, CourseDetailSerializer,
    LessonSerializer, EnrollmentSerializer, CertificateSerializer,
    TeacherProfileSerializer, DirectorProfileSerializer, StudentGroupSerializer,
    JournalEntrySerializer, VideoLessonSerializer
)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().prefetch_related("lessons")
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action in ["list"]:
            return CourseListSerializer
        return CourseDetailSerializer

    permission_classes = [permissions.AllowAny]

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # студент видит только свои записи; админ — все
        user = self.request.user
        if user.is_staff:
            return Enrollment.objects.all()
        return Enrollment.objects.filter(student=user)

    def perform_create(self, serializer):
        serializer.save()  # create() в сериализаторе обработает student

class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Certificate.objects.select_related("enrollment__student", "enrollment__course").all()
    serializer_class = CertificateSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["get"], url_path="by-number")
    def by_number(self, request):
        num = request.query_params.get("q")
        if not num:
            return Response({"detail":"provide ?q=cert_number"}, status=status.HTTP_400_BAD_REQUEST)
        cert = self.get_queryset().filter(cert_number=num).first()
        if not cert:
            return Response({"detail":"not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(cert).data)


class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class DirectorProfileViewSet(viewsets.ModelViewSet):
    queryset = DirectorProfile.objects.all()
    serializer_class = DirectorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentGroupViewSet(viewsets.ModelViewSet):
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class JournalEntryViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]


class VideoLessonViewSet(viewsets.ModelViewSet):
    queryset = VideoLesson.objects.all()
    serializer_class = VideoLessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        teacher_profile = self.request.user.teacher_profile
        serializer.save(teacher=teacher_profile)