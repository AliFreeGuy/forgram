from django.db import models
from accounts.models import User
from .forgram import ForGramModel


class ForGramMessageSenderModel(models.Model):
    message = models.TextField()
    forgram = models.ForeignKey(ForGramModel , on_delete=models.CASCADE )
    created = models.DateTimeField(auto_now=True , null=True , blank=True)
    is_completed = models.BooleanField(default=False )



    def __str__(self):
        return str(self.message)
    
    class Meta :

        verbose_name = "Send message"
        verbose_name_plural = "Send message"