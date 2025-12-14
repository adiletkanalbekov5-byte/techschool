# core/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (Course,
                     Lesson,
                     Enrollment,
                     Certificate,
                     TeacherProfile,
                     DirectorProfile,
                     StudentGroup,
                     JournalEntry,
                     VideoLesson,
                     Application)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','is_staff','is_active']
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('created_at','user')
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "order", "video_url", "content"]

class CourseListSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source="lessons.count", read_only=True)
    class Meta:
        model = Course
        fields = ["id", "title", "slug", "description", "level", "price", "lessons_count", "cover"]

class CourseDetailSerializer(CourseListSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    class Meta(CourseListSerializer.Meta):
        fields = CourseListSerializer.Meta.fields + ["lessons"]

class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    course = CourseListSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True, source="course")
    class Meta:
        model = Enrollment
        fields = ["id", "student", "course", "course_id", "active", "purchased_at"]
        read_only_fields = ["id", "student", "course", "purchased_at"]

    def create(self, validated_data):
        student = self.context["request"].user
        course = validated_data["course"]
        enrollment, created = Enrollment.objects.get_or_create(student=student, course=course)
        return enrollment

class CertificateSerializer(serializers.ModelSerializer):
    enrollment = EnrollmentSerializer(read_only=True)
    class Meta:
        model = Certificate
        fields = ["id", "cert_number", "issued_at", "enrollment"]
class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        write_only=True,
        source="user",
        required=False
    )
    class Meta:
        model = TeacherProfile
        fields = ['id','user','user_id','bio','phone']

class DirectorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorProfile
        fields = ['id','user','phone']

class StudentGroupSerializer(serializers.ModelSerializer):
    teacher = TeacherProfileSerializer(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=TeacherProfile.objects.all(),
        write_only=True,
        source="teacher",
        required=False
    )
    students = serializers.StringRelatedField(many=True, read_only=True)
    student_ids = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        many=True,
        write_only=True,
        source="students",
        required=False
    )
    student_ids_read = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        source="students"
    )

    class Meta:
        model = StudentGroup
        fields = ['id','name','teacher','teacher_id','students','student_ids','student_ids_read']

class JournalEntrySerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    group = serializers.StringRelatedField()
    group_id = serializers.IntegerField(source="group.id", read_only=True)
    group_teacher_id = serializers.IntegerField(source="group.teacher.id", read_only=True)
    class Meta:
        model = JournalEntry
        fields = ['id','student','group','group_id','group_teacher_id','date','grade','comment']

class VideoLessonSerializer(serializers.ModelSerializer):
    teacher = TeacherProfileSerializer(read_only=True)
    class Meta:
        model = VideoLesson
        fields = ['id','course','title','video_file','created_at','teacher']