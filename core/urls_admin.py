from django.urls import path
from . import views_admin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


urlpatterns = [
    path("", views_admin.admin_panel, name="admin_panel"),
]

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    return render(request, "admin_panel.html")
