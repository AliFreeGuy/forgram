from django.db import models
from accounts.models import User


class ForGramRefUsers(models.Model):
    inviting_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='inviting_user' , null=True , blank=True)
    invited_user = models.ForeignKey(User , on_delete=models.CASCADE , null=True , blank=True , related_name='invited_user')
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return str(self.inviting_user)
    class Meta:

        verbose_name = "User invitation"
        verbose_name_plural = "User invitations"