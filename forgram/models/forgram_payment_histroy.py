from django.db import models
from . import ForGramModel
from accounts.models import User


class ForGramPaymentHistoryModel(models.Model):
    forgram = models.ForeignKey(ForGramModel , on_delete=models.CASCADE , related_name='payment_history')
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='payment_history')
    amount = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    cart_number = models.CharField(max_length=128 , null=True , blank=True )
    notes =  models.TextField(null=True , blank=True)
    approval_date = models.DateTimeField(null=True , blank=True)
    request_date = models.DateTimeField(auto_now=True)



    def __str__(self) -> str:
        return str(self.user)
    
        
    class Meta:
        ordering = ['-request_date']

        verbose_name = "Payment history"
        verbose_name_plural = "Payment history"