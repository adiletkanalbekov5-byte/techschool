from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    return render(request, "admin_panel.html")
