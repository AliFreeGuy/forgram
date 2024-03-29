from django.contrib.auth.models import BaseUserManager




class UserManager(BaseUserManager):
    def create_user(self , username , phone_number  , full_name, password ):
        if not username :
            raise ValueError('user must have username')
        if not phone_number :
            raise ValueError('user must have phone_number')
        if not full_name :
            raise ValueError('user must have full_name')
        
        user = self.model(username = username , phone_number = phone_number  , full_name = full_name)
        user.set_password(password)
        user.save(using = self._db)
        return user
    


    def create_superuser(self , username , phone_number , full_name , password):
        user = self.create_user(username , phone_number , full_name , password)
        user.is_admin = True
        user.save(using = self._db)
        return user
    

    def get_sub(self, user):
        try:
            return user.sub.filter(is_active=True).first()
        except:
            return None
    