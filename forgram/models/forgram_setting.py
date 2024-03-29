from django.db import models
from . import ForGramModel


class ForGramSettingModel(models.Model):
    forgram = models.ForeignKey(ForGramModel , on_delete=models.CASCADE , related_name='settings')
    name = models.CharField(max_length=128 , unique=True)
    setting = models.JSONField()


    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:

        verbose_name = "Setting"
        verbose_name_plural = "Setting"