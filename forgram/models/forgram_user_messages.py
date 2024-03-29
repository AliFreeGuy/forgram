from django.db import models
from accounts.models import User


class ForGramUserMessageModel(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='message')
    message = models.JSONField()
    date = models.DateTimeField(auto_now=True)
    type = models.CharField(default='message' ,null=True , blank=True , max_length=16)
    message_id = models.IntegerField(null=True , blank=True)
    created = models.DateTimeField(auto_now=True , null=True , blank=True)
    
    def __str__(self) -> str:
        return str(self.user)
    
    
    class Meta:

        ordering = ['-created',]
        verbose_name = "User Message"
        verbose_name_plural = "User Message"