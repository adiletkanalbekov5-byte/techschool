# core/urls.py
from django.urls import path, include
from rest_framework import routers
from . import views
from django.views.generic import TemplateView

# Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from core.views import AdminApplicationViewSet, AdminUserViewSet
router = routers.DefaultRouter()
router.register(r"courses", views.CourseViewSet, basename="courses")
router.register(r"lessons", views.LessonViewSet)
router.register(r"enrollments", views.EnrollmentViewSet, basename="enrollments")
router.register(r"certificates", views.CertificateViewSet, basename="certificates")
router.register(r'teachers', views.TeacherProfileViewSet)
router.register(r'directors', views.DirectorProfileViewSet)
router.register(r'groups', views.StudentGroupViewSet)
router.register(r'journal', views.JournalEntryViewSet)
router.register(r'videos', views.VideoLessonViewSet)
router.register(r"admin/applications", AdminApplicationViewSet, basename="admin-applications")
router.register(r"admin/users", AdminUserViewSet, basename="admin-users")
schema_view = get_schema_view(
   openapi.Info(title="TechSchool API", default_version='v1', description="API для онлайн-школы"),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # HTML pages (простые)
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("courses/", TemplateView.as_view(template_name="courses_list.html"), name="courses_list"),
    path("courses/<slug:slug>/", TemplateView.as_view(template_name="course_detail.html"), name="course_detail"),


    # Профили
    path("teacher_profile/", TemplateView.as_view(template_name="teacher_profile.html"), name="teacher_profile"),
    path("teacher_profile/<int:pk>/", TemplateView.as_view(template_name="teacher_profile.html"), name="teacher_profile_detail"),
    path("teacher_profile/<int:pk>/journal/", TemplateView.as_view(template_name="teacher_journal.html"), name="teacher_journal"),
    path("teacher_profile/<int:pk>/add_student/", TemplateView.as_view(template_name="teacher_add_student.html"), name="teacher_add_student"),
    path("director_profile/", TemplateView.as_view(template_name="director_profile.html"), name="director_profile"),
    path("admin_panel/", TemplateView.as_view(template_name="admin_panel.html"), name="admin_panel"),
    # Видео уроки
    path("videos_page/", TemplateView.as_view(template_name="videos_page.html"), name="videos_page"),

    # API
    path("api/", include(router.urls)),
    path("admin-panel/", include("core.urls_admin")),
    # Browsable API login
    path("api/auth/", include("rest_framework.urls")),

    # JWT (правильно!!)
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Swagger UI
    path(r"swagger(?P<format>\.json|\.yaml)", schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

