from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from accounts.managers import UserManager
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin


class User(AbstractBaseUser , PermissionsMixin):
    username = models.CharField(max_length=32 , unique=True)
    phone_number = models.CharField(max_length=16 , unique=True ,null=True , blank=True)
    full_name = models.CharField(max_length=128)
    cart_number = models.CharField(max_length=64 , null=True , blank=True)
    creation= models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_join = models.BooleanField(default=True  , null= True , blank=True)


    objects  = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number' , 'full_name' ,]


    def __str__(self) -> str:
        return str(f'{self.username} - {self.full_name}')
    
    def has_perm(self, perm, obj=None):
                return self.is_admin

    def has_module_perms(self, app_label):
                return True
    
    @property
    def is_staff(self ):
        return self.is_admin

    def get_sub(self):
        return UserManager().get_sub(self)
