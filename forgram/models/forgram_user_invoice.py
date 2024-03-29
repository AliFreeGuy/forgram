from django.db import models
from accounts.models import User
from .forgram import ForGramModel 
from .forgram_plans import ForgramPlansModel
from django.db.models import Q






class ForgramUserInvoiceModel(models.Model):
    STATUS_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('paying', 'Paying'),
    )
    forgram = models.ForeignKey(ForGramModel , on_delete=models.CASCADE )
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='invoice' , null=True , blank=True)
    plan = models.ForeignKey(ForgramPlansModel , on_delete=models.CASCADE , null=True , blank=True)
    buyer_user = models.ForeignKey(User , on_delete=models.CASCADE , null= True , blank=True)
    created_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    is_paid = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid' , null=True , blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    notes = models.TextField(null=True, blank=True)
    is_discount = models.BooleanField(default=False)

    def get_total_paid(self):
        paid_invoices = ForgramUserInvoiceModel.objects.filter(is_paid='paid')
        total_paid_amount = sum(invoice.amount for invoice in paid_invoices)
        return round(total_paid_amount, 0)
        


    def get_total_unpaid(self):
        unpaid_or_paying_invoices = ForgramUserInvoiceModel.objects.filter(Q(is_paid='unpaid') | Q(is_paid='paying'))
        total_unpaid_amount = sum(invoice.amount for invoice in unpaid_or_paying_invoices)
        return round(total_unpaid_amount, 0)
    
    class Meta:
        ordering = ['-created_at']

        verbose_name = "User invoice"
        verbose_name_plural = "User invoice"

