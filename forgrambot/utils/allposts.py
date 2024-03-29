
import sys

instance_id = sys.argv[1:][0]

proxy = {"scheme": "socks5","hostname": "127.0.0.1","port": 1080,}

import sys
import os
import django

sys.dont_write_bytecode = True
script_path = os.path.dirname(__file__)
project_dir = os.path.abspath(os.path.join(script_path, '..','..', '..','web'))

sys.path.insert(0, project_dir)
os.environ['DJANGO_SETTINGS_MODULE']='web.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from pyrogram import Client 
import time
from accounts.models import User
from forgram import models
forgram = models.ForGramModel.objects.first()
api_hash = forgram.api_hash
api_id =  forgram.api_id
bot_token = forgram.bot_token




try :
    instance = models.ForGramForwarderAdvanceModel.objects.get(pk = instance_id)

    bot = Client('asd' , api_hash=api_hash , api_id=api_id , bot_token=bot_token , proxy=proxy)
    bot.start()
    for i in range(5) :


       
        
        bot.send_message('accroot' ,f'{User.objects.first().username} - {instance.user}' )
        print('sended ')
        time.sleep(1)
    bot.stop()
    instance.status = 'completed'
    instance.save()
except Exception as e :
    print(e)



