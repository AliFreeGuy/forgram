from django.db import models



class ForGramModel(models.Model):
    username = models.CharField(max_length=128)
    bot_token = models.CharField(max_length=128)
    api_id = models.CharField(max_length=128)
    api_hash = models.CharField(max_length=128 )



    def __str__(self) -> str:
        return str(self.username)
    
    class Meta:

        verbose_name = "Forgram Data"
        verbose_name_plural = "Forgram Data"