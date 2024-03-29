from django.db import models
from accounts.models import User
from .forgram import ForGramModel 
from .forgram_plans import ForgramPlansModel
from django.utils import timezone
import datetime

class SubForGramUserModel(models.Model):
    forgram = models.ForeignKey(ForGramModel , on_delete=models.CASCADE )
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='sub' , null=True , blank=True)
    plan= models.ForeignKey(ForgramPlansModel , on_delete=models.CASCADE  , null=True , blank=True)
    expiry = models.DateTimeField(null=True , blank=True)
    volum = models.IntegerField(default=0 , null= True , blank=True)
    volum_used = models.IntegerField(default=0 , null=True , blank = True)
    is_active = models.BooleanField(default=True)



    @property
    def re_volum(self):
        return int(int(self.volum )- int(self.volum_used))
    

    def decrease(self, amount):
            self.volum_used+= amount
            self.save()



    def save(self, *args, **kwargs):
        data = SubForGramUserModel.objects.filter(id = self.id)
        if self.plan and  not data.exists() :
                self.expiry = datetime.datetime.now() + datetime.timedelta(days=int(self.plan.day))
                self.volum = self.plan.volum
                if self.user and self.user.sub.filter(is_active=True).exists():
                    self.user.sub.filter(is_active=True).update(is_active=False)
                    self.is_active = True

        if self.plan and data.exists():
            now = timezone.now()
            sub_expiry = self.expiry
            if now > sub_expiry :
                free_plan = ForgramPlansModel.objects.get(tag = 'free')
                self.is_active = False
                SubForGramUserModel.objects.create(forgram = self.forgram , user = self.user , plan = free_plan)
                
             


        super().save(*args, **kwargs)


    def __str__(self) -> str:
        return str(self.user)
    
    class Meta :

        verbose_name = "User Subscription"
        verbose_name_plural = "User Subscription"