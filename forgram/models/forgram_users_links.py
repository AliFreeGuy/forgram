from django.db import models
from . import ForGramModel
from accounts.models import User

class ForGramUserLinkModel(models.Model):
    forgram = models.ForeignKey(ForGramModel , on_delete=models.CASCADE , related_name='link')
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='link')
    link = models.CharField(max_length=1024 , null=True , blank=True)
    is_complete= models.BooleanField(default=False )   
    created = models.DateTimeField(auto_now=True , null=True , blank=True)


    def __str__(self) -> str:
        return self.link
    
    class Meta :
        ordering = ['-created']
        verbose_name = "User links"
        verbose_name_plural = "User links"