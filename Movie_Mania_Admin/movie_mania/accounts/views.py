import random
import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, OTP


# Create your views here.
#sent otp
@api_view(["POST"])
def send_otp(request):
    identifier = request.data.get("identifier")  # email or phone

    if not identifier:
        return Response({"error": "Email or phone required"}, status=400)

    # Detect email
    if "@" in identifier:
        try:
            user = User.objects.get(email=identifier, role="admin")
        except User.DoesNotExist:
            return Response({"error": "Admin not found"}, status=404)

    # Detect phone
    else:
        try:
            user = User.objects.get(phone=identifier, role="admin")
        except User.DoesNotExist:
            return Response({"error": "Admin not found"}, status=404)

    otp = str(random.randint(100000, 999999))
    OTP.objects.create(user=user, otp=otp)

    print("OTP:", otp)  

    return Response({"message": "OTP sent"})



#reset otp
@api_view(["POST"])
def reset_password(request):
    identifier = request.data.get("identifier")
    otp = request.data.get("otp")
    new_password = request.data.get("new_password")

    user = None
    if "@" in identifier:
        user = User.objects.filter(email=identifier, role="admin").first()
    else:
        user = User.objects.filter(phone=identifier, role="admin").first()

    if not user:
        return Response({"error": "Admin not found"}, status=404)

    otp_obj = OTP.objects.filter(user=user, otp=otp).order_by("-created_at").first()
    if not otp_obj:
        return Response({"error": "Invalid OTP"}, status=400)

    user.set_password(new_password)
    user.save()
    otp_obj.delete()

    return Response({"message": "Password reset successful"})
