from django.urls import path, include
from rest_framework import routers
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views
from core.views import AdminApplicationViewSet, AdminUserViewSet


# =========================
# API ROUTER
# =========================

router = routers.DefaultRouter()
router.register(r"courses", views.CourseViewSet, basename="courses")
router.register(r"lessons", views.LessonViewSet)
router.register(r"enrollments", views.EnrollmentViewSet, basename="enrollments")
router.register(r"certificates", views.CertificateViewSet, basename="certificates")
router.register(r"teachers", views.TeacherProfileViewSet)
router.register(r"directors", views.DirectorProfileViewSet)
router.register(r"groups", views.StudentGroupViewSet, basename="groups")
router.register(r"journal", views.JournalEntryViewSet, basename="journal")
router.register(r"videos", views.VideoLessonViewSet)

# Admin API
router.register(r"admin/applications", AdminApplicationViewSet, basename="admin-applications")
router.register(r"admin/users", AdminUserViewSet, basename="admin-users")


# =========================
# SWAGGER
# =========================

schema_view = get_schema_view(
    openapi.Info(
        title="TechSchool API",
        default_version="v1",
        description="API для онлайн-школы",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# =========================
# URLS
# =========================

urlpatterns = [
    # -------- HTML --------
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("courses/", TemplateView.as_view(template_name="courses_list.html"), name="courses_list"),
    path("courses/<slug:slug>/", TemplateView.as_view(template_name="course_detail.html"), name="course_detail"),

    # ====== УЧИТЕЛЬ (только после логина) ======
    path(
        "teacher_profile/",
        login_required(TemplateView.as_view(template_name="teacher_profile.html")),
        name="teacher_profile",
    ),
    path(
        "teacher_profile/<int:pk>/journal/",
        login_required(TemplateView.as_view(template_name="teacher_journal.html")),
        name="teacher_journal",
    ),

    # ====== ДИРЕКТОР ======
    path(
        "director/",
        login_required(TemplateView.as_view(template_name="director_profile.html")),
        name="director_profile",
    ),

    # ====== АДМИН (HTML) ======
    path(
        "admin-panel/",
        login_required(TemplateView.as_view(template_name="admin_panel.html")),
        name="admin_panel",
    ),

    # Видео
    path(
        "videos/",
        TemplateView.as_view(template_name="videos_page.html"),
        name="videos_page",
    ),

    # -------- API --------
    path("api/", include(router.urls)),

    # Browsable API login
    path("api/auth/", include("rest_framework.urls")),

    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # -------- SWAGGER --------
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
