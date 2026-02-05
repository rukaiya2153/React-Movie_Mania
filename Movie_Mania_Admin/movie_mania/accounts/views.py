from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.db.models import Sum
import random

from accounts.models import User, OTP, LoginAttempt
from movies.models import Movie
from shows.models import Show           # Correct import from shows app
from payments.models import Payment


# ---------------- LOGIN ----------------
@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    phone = request.data.get("phone")

    if not username or not password:
        return Response({"error": "Username and password required"}, status=400)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Invalid credentials"}, status=400)

    # Save/update phone number and last login
    if phone:
        user.phone = phone
    user.last_login = timezone.now()
    user.save()

    # Log the login attempt
    LoginAttempt.objects.create(
        user=user,
        phone=phone
    )

    # Return JWT tokens
    refresh = RefreshToken.for_user(user)
    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "message": "Login successful"
    })


# ---------------- SEND OTP ----------------
@api_view(["POST"])
def send_otp(request):
    identifier = request.data.get("identifier")
    if not identifier:
        return Response({"error": "Email or phone required"}, status=400)

    user = None
    if "@" in identifier:
        user = User.objects.filter(email=identifier, role="admin").first()
    elif identifier.isdigit():
        user = User.objects.filter(phone=identifier, role="admin").first()

    if not user:
        return Response({"error": "Admin not found"}, status=404)

    otp_code = str(random.randint(100000, 999999))
    OTP.objects.create(user=user, otp=otp_code)
    print("OTP:", otp_code)  # Replace with real SMS/email in production
    return Response({"message": "OTP sent"})


# ---------------- RESET PASSWORD ----------------
@api_view(["POST"])
def reset_password(request):
    identifier = request.data.get("identifier")
    otp = request.data.get("otp")
    new_password = request.data.get("new_password")

    user = None
    if "@" in identifier:
        user = User.objects.filter(email=identifier, role="admin").first()
    elif identifier.isdigit():
        user = User.objects.filter(phone=identifier, role="admin").first()

    if not user:
        return Response({"error": "Admin not found"}, status=404)

    otp_obj = OTP.objects.filter(user=user, otp=otp).first()
    if not otp_obj:
        return Response({"error": "Invalid OTP"}, status=400)

    user.set_password(new_password)
    user.save()
    otp_obj.delete()
    return Response({"message": "Password reset successful"})


# ---------------- DASHBOARD DATA ----------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_data(request):
    admin = request.user
    total_movies = Movie.objects.count()
    total_shows = Show.objects.count()
    total_users = User.objects.filter(role="user").count()
    total_revenue = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0

    # Latest 5 uploads
    recent_uploads = Movie.objects.order_by('-created_at')[:5]
    recent_list = [
        {"title": m.title, "views": getattr(m, "views", 0)}
        for m in recent_uploads
    ]

    return Response({
        "admin_name": admin.username,
        "total_movies": total_movies,
        "total_shows": total_shows,
        "total_users": total_users,
        "total_revenue": total_revenue,
        "recent_uploads": recent_list
    })
