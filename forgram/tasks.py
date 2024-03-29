from celery import shared_task 
from accounts.models import User
from forgram.models import ForGramModel , ForGramMessageSenderModel
import requests
import time



@shared_task
def send_message_task(message):
    try :
        users  = User.objects.all()
        forgram = ForGramModel.objects.first()
        for user in users :
        
            print(f'SENDED >>> {user.username}')
            
            url = f'https://api.telegram.org/bot{forgram.bot_token}/sendMessage'
            payload = {'chat_id':user.username ,'text': message}
            response = requests.post(url, data=payload )
            
        msg = ForGramMessageSenderModel.objects.filter(message = message)
        if msg.exists() :
            msg = msg[0]
            msg.is_completed = True
            msg.save()
    except :pass
        
                     
		