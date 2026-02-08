from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.db.models import Sum, Q
import random

from .models import User, OTP, LoginAttempt
from movies.models import Movie
from shows.models import Show
from payments.models import Payment
from django.shortcuts import render



# ---------------- LOGIN API ----------------
@api_view(["POST"])
@permission_classes([AllowAny])   # 🔥 VERY IMPORTANT FIX
def login_view(request):
    identifier = request.data.get("username")  # username or phone
    password = request.data.get("password")
    phone = request.data.get("phone")  # optional

    if not identifier or not password:
        return Response(
            {"error": "Username/phone and password required"},
            status=400
        )

    # Find user by username OR phone
    user_obj = User.objects.filter(
        Q(username=identifier) | Q(phone=identifier)
    ).first()

    if not user_obj:
        return Response({"error": "Invalid credentials"}, status=401)

    # Authenticate using username (required by Django)
    user = authenticate(
        username=user_obj.username,
        password=password
    )

    if not user:
        return Response({"error": "Invalid credentials"}, status=401)

    # Admin-only login
    if user.role != "admin":
        return Response({"error": "Admin access only"}, status=403)

    # Optional phone update
    if phone:
        user.phone = phone

    user.last_login = timezone.now()
    user.save()

    # Log login
    LoginAttempt.objects.create(
        user=user,
        phone=phone
    )

    # JWT tokens
    refresh = RefreshToken.for_user(user)

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "message": "Login successful"
    })


# ---------------- SEND OTP ----------------
@api_view(["POST"])
@permission_classes([AllowAny])
def send_otp(request):
    identifier = request.data.get("identifier")

    if not identifier:
        return Response({"error": "Email or phone required"}, status=400)

    if "@" in identifier:
        user = User.objects.filter(email=identifier, role="admin").first()
    else:
        user = User.objects.filter(phone=identifier, role="admin").first()

    if not user:
        return Response({"error": "Admin not found"}, status=404)

    otp_code = str(random.randint(100000, 999999))
    OTP.objects.create(user=user, otp=otp_code)

    print("OTP (DEV ONLY):", otp_code)

    return Response({"message": "OTP sent"})


# ---------------- RESET PASSWORD ----------------
@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request):
    identifier = request.data.get("identifier")
    otp_val = request.data.get("otp")
    new_password = request.data.get("new_password")

    if not identifier or not otp_val or not new_password:
        return Response({"error": "All fields required"}, status=400)

    if "@" in identifier:
        user = User.objects.filter(email=identifier, role="admin").first()
    else:
        user = User.objects.filter(phone=identifier, role="admin").first()

    if not user:
        return Response({"error": "Admin not found"}, status=404)

    otp_obj = OTP.objects.filter(user=user, otp=otp_val).first()
    if not otp_obj:
        return Response({"error": "Invalid OTP"}, status=400)

    user.set_password(new_password)
    user.save()
    otp_obj.delete()

    return Response({"message": "Password reset successful"})


# ---------------- DASHBOARD API ----------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_data(request):
    admin = request.user

    total_movies = Movie.objects.count()
    total_shows = Show.objects.count()
    total_users = User.objects.filter(role="user").count()
    total_revenue = Payment.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    recent_uploads = Movie.objects.order_by("-created_at")[:5]
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


def dashboard_page(request):
    return render(request, "dashboard.html")


def movies_page(request):
    return render(request, "movies.html")


def tvshows_page(request):
    return render(request, "tvshows.html")


def genres_page(request):
    return render(request, "genres.html")


def users_page(request):
    return render(request, "users.html")


def payments_page(request):
    return render(request, "payments.html")


def reports_page(request):
    return render(request, "reports.html")

