from django.db import models
from accounts.models import User
from .forgram import ForGramModel


class ForGramUsersModel(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name='fg' , unique=True)
    forgram = models.ForeignKey(ForGramModel , on_delete=models.CASCADE )
    created = models.DateTimeField(auto_now=True , null=True , blank=True)
    def __str__(self):
        return str(self.user)
    class Meta:

        verbose_name = "User"
        verbose_name_plural = "User"