from django.urls import path
from .views import send_otp, reset_password

urlpatterns = [
    path("send-otp/", send_otp),
    path("reset-password/", reset_password),
]
