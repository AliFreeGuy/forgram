from config import db
import json
from pyrogram.types import Message , CallbackQuery
from django.utils import timezone



def user_updater(func):
    async def wrapper(client, message):
        user = None 
        username = message.from_user.id
        if message.from_user.last_name and message.from_user.first_name:
            full_name = f'{message.from_user.first_name} {message.from_user.last_name}'
        elif message.from_user.last_name == None or message.from_user.first_name == None:
            if message.from_user.first_name != None:full_name = message.from_user.first_name
            else:full_name = message.from_user.last_name
        else:
            full_name = str(message.from_user.id)


        
        try:
            user = db.User.objects.get(username=username)
            user.full_name = full_name
            user.save()
            
        except db.User.DoesNotExist:
            user = db.User.objects.create(username=username, full_name=full_name, password=username)
            
        try :
            message_save = db.ForGramUserMessageModel(user = user , message = json.loads(str(message)))
            if type(message) is CallbackQuery :
                message_save.type = 'call'
                message_save.message_id = int(message.message.id)
            else :
                message_save.message_id = int(message.id)
            
            message_save.save()
        except :pass
        if not db.ForGramUsersModel.objects.filter(user = user ).exists():
            forgram = db.ForGramModel.objects.first()
            db.ForGramUsersModel(user = user , forgram = forgram ).save()




        user = db.User.objects.get(username = username)
        user_sub = user.get_sub()
        free_plan = db.ForgramPlansModel.objects.get(tag='free')
        forgram = db.ForGramModel.objects.first()
        if user_sub is not None and timezone.now() > user_sub.expiry:
            user_sub.save()
        elif user_sub is None:
            db.SubForGramUserModel.objects.create(user=user, plan=free_plan , forgram = forgram)
        




        await func(client, message, user)
    return wrapper