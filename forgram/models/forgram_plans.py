from django.db import models
from . import ForGramModel


class ForgramPlansModel(models.Model):
    forgram = models.ForeignKey(ForGramModel , on_delete=models.CASCADE , related_name='plans')
    tag = models.CharField(max_length=128 , unique=True)
    name = models.CharField(max_length=128 , unique=True)
    day = models.IntegerField(default=0 )
    volum = models.IntegerField(default=0 , null=True ,blank = True)
    description = models.TextField()
    price = models.IntegerField(default=0 , null=True , blank=True)
    discount = models.IntegerField(default=0 , null=True , blank=True)
    is_discount = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    def __str__(self) -> str:
        return str(self.tag)
    
    
    
    class Meta:

        verbose_name = "Plan"
        verbose_name_plural = "Plans"