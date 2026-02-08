from django.urls import path
from .views import login_view, send_otp, reset_password, dashboard_data

urlpatterns = [
    path("login/", login_view, name="login"),
    path("send-otp/", send_otp, name="send_otp"),
    path("reset-password/", reset_password, name="reset_password"),
    path("dashboard/", dashboard_data, name="dashboard-data"),
]
