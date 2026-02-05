from rest_framework.decorators import api_view
from rest_framework.response import Response
from movies.models import Movie
from payments.models import Payment
from accounts.models import User
from django.db.models import Sum

@api_view(['GET'])
def admin_dashboard(request):
    return Response({
        "total_movies": Movie.objects.count(),
        "total_users": User.objects.count(),
        "total_revenue": Payment.objects.filter(
            payment_status='success'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
    })
