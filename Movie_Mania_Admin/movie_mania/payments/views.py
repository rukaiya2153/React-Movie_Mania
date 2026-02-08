from rest_framework.viewsets import ModelViewSet
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.permissions import IsAdminUser

class PaymentAdminViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ["get"]   # READ ONLY
