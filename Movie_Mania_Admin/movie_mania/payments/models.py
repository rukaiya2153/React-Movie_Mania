from django.db import models
from accounts.models import User

class Payment(models.Model):
    STATUS = (
        ('success','Success'),
        ('failed','Failed'),
        ('pending','Pending')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=STATUS)
    payment_date = models.DateTimeField(auto_now_add=True)
