from django.db import models
from accounts.models import User


class ForGramUserSession(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='session')
    session_name = models.CharField(max_length=128)
    password = models.CharField(max_length=128 , null=True , blank=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.user)
    

    class Meta :


        # add ordering['-created',]
        verbose_name = "User session"
        verbose_name_plural = "User session"