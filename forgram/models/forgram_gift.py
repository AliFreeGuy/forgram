from django.db import models
from . import ForGramModel
from accounts.models import User


class ForGramGiftModel(models.Model):
    forgram = models.ForeignKey(ForGramModel , on_delete=models.CASCADE , related_name='gift')
    code = models.CharField(max_length=128)
    count = models.IntegerField(default=100)
    used = models.IntegerField(default=0)
    volum = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.code)
    
    class Meta:
        ordering = ['-created' , ]


        verbose_name = "Gitf"
        verbose_name_plural = "Gift"

class ForGramUseGift(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='gift')
    gift = models.ForeignKey(ForGramGiftModel , related_name='gift_used' , on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user} - {self.gift}'

    class Meta :
        ordering = ['-created' ,]
        verbose_name = "Gitf Used"
        verbose_name_plural = "Gift Used"