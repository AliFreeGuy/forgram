from celery import Celery
from pyrogram import Client
import os
import redis
import time
import math
import random
import sys
import requests
import django
from pyrogram.errors import AuthKeyUnregistered
from pyrogram.enums import MessageMediaType 
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', '..','web')))
os.environ['DJANGO_SETTINGS_MODULE']='web.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from accounts.models import User
from forgram.models import ForGramModel , ForGramUserLinkModel



forgram = ForGramModel.objects.first()
api_hash = forgram.api_hash
api_id =  forgram.api_id
bot_token = forgram.bot_token
proxy = {"scheme": "socks5","hostname": "127.0.0.1","port": 1080,}
admin = 5111632400

r = redis.Redis(host='localhost', port=6379, db=8)
 

app = Celery('forgram_worker' , backend='redis://localhost:6379/5' , broker='redis://localhost:6379/5')
app.conf.update(
    task_serializer = 'pickle' , 
    result_serializer = 'pickle' , 
    accept_content = ['application/x-python-serialize'],
    worker_concurrency = 1,
    worker_prefetch_multiplier = 1,
)

base_dir = os.getcwd()






@app.task(name='forgram_worker.downloader' , bind = True , default_retry_delay=1)
def downloader(self , user_id , link , message_id=None  ) : 
    try :

        last_link = link
        user = User.objects.filter(username = user_id)
        if user.exists():
            user = user[0]
            user_sessions = user.session.last()
            

            if user_sessions :
                
                session_dir = f'{base_dir}/{user_sessions.session_name}'
                
                try :
                        client = Client(session_dir , api_hash=api_hash , api_id=api_id ,app_version='2.0.0' , device_model='self bot' )
                        client.connect()
                        link = link.replace('?single' , '')
                        link = link.replace('https://t.me/' , '').split('/')
                        if len(link) == 3 : 
                                msg_id = int(link[2])
                                chat_id = int(f'-100{link[1]}')
                        elif len(link) == 2 : 
                                msg_id = int(link[1])
                                chat_id = link[0]

                        msg = client.get_messages(chat_id=chat_id , message_ids=msg_id)
                        link_data = ForGramUserLinkModel.objects.filter(user = user , link = last_link)
                        if link_data.exists():
                                link_data = link_data.first()
                        else :
                               link_data = False
                        
                        
                        if msg.empty != True :
                                media = str(msg.media )
                                
                                
                                if msg.chat.has_protected_content :
                                        if media == 'None' : 
                                                send = client.send_message('me' , msg.text)
                                                edit_message(chat_id=user_id , message_id=message_id , text = '✅ با موفقیت انجام شد ')
                                                link_data.is_complete = True
                                                link_data.save()

                                        elif media == 'MessageMediaType.PHOTO' : 
                                                file_size = math.ceil(msg.photo.file_size  / (1024*1024))
                                                file_name = f'{str(random.randint(3333 , 3333344))}.jpg'
                                                volume = user.get_sub().re_volum
                                                if int(volume)  > file_size : 
                                                        client.download_media(msg ,file_name=base_dir + f'/downloads/{file_name}')
                                                        user.get_sub().decrease(file_size) 
                                                        send = client.send_photo(chat_id= 'me' , photo=base_dir + f'/downloads/{file_name}' ,caption=msg.caption)
                                                        if os.path.exists(base_dir + f'/downloads/{file_name}'):
                                                                os.remove(base_dir + f'/downloads/{file_name}')
                                                        edit_message(chat_id=user_id , message_id=message_id , text = '✅ با موفقیت انجام شد ')
                                                        link_data.is_complete = True
                                                        link_data.save()
                                                else :send_message(chat_id=user_id , text = 'حجم دانلود شما ناکافی است برای افزایش حجم اشتراک تهیه کنید')

                                        elif media == 'MessageMediaType.VIDEO': 
                                                file_size  = math.ceil(msg.video.file_size  / (1024*1024))
                                                file_name = str(random.randint(999 , 9999)) + '.' +msg.video.mime_type.split('/')[1]
                                                volume = user.get_sub().re_volum

                                                if int(volume)  > file_size : 
                                                        client.download_media(msg ,file_name=base_dir + f'/downloads/{file_name}')
                                                        user.get_sub().decrease(file_size) 

                                                        client.send_video(chat_id='me' , video = base_dir + f'/downloads/{file_name}' , caption=msg.caption)
                                                        if os.path.exists(base_dir + f'/downloads/{file_name}'):
                                                                os.remove(base_dir + f'/downloads/{file_name}')
                                                        edit_message(chat_id=user_id , message_id=message_id , text = '✅ با موفقیت انجام شد ')
                                                        link_data.is_complete = True
                                                        link_data.save()
                                                else :send_message(chat_id=user_id , text = 'حجم دانلود شما ناکافی است برای افزایش حجم اشتراک تهیه کنید')
                                

                                        elif media =='MessageMediaType.DOCUMENT': 
                                                file_size  = math.ceil(msg.document.file_size  / (1024*1024))
                                                file_name = str(random.randint(999 , 9999)) + '.' +msg.document.file_name
                                                volume = user.get_sub().re_volum
                                                if int(volume)  > file_size : 
                                                        print('3#############################################')

                                                        print(f'VOLUME : {str(volume)}')
                                                        print(f'file_size : {str(file_size)}')
                                                        print('3#############################################')
                                                        data = user.get_sub().decrease(file_size)

                                                        print(data)
                                                        client.download_media(msg ,file_name=base_dir + f'/downloads/{file_name}')
                                                        
                                                        

                                                        client.send_document(chat_id='me' , document = base_dir + f'/downloads/{file_name}' , caption=msg.caption)
                                                        if os.path.exists(base_dir + f'/downloads/{file_name}'):
                                                                os.remove(base_dir + f'/downloads/{file_name}')
                                                        edit_message(chat_id=user_id , message_id=message_id , text = '✅ با موفقیت انجام شد ')
                                                        link_data.is_complete = True
                                                        link_data.save()
                                                else :send_message(chat_id=user_id , text = 'حجم دانلود شما ناکافی است برای افزایش حجم اشتراک تهیه کنید')


                                        elif media == 'MessageMediaType.ANIMATION':
                                                file_size  = math.ceil(msg.animation.file_size  / (1024*1024))
                                                file_name = str(random.randint(999 , 9999)) + '.' +msg.animation.mime_type.split('/')[1]
                                                volume = user.get_sub().re_volum

                                                if int(volume)  > file_size : 
                                                        client.download_media(msg ,file_name=base_dir + f'/downloads/{file_name}')
                                                        user.get_sub().decrease(file_size) 

                                                        client.send_document(chat_id='me' , document = base_dir + f'/downloads/{file_name}')
                                                        if os.path.exists(base_dir + f'/downloads/{file_name}'):
                                                                os.remove(base_dir + f'/downloads/{file_name}')
                                                        edit_message(chat_id=user_id , message_id=message_id , text = '✅ با موفقیت انجام شد ')
                                                        link_data.is_complete = True
                                                        link_data.save()
                                                else :send_message(chat_id=user_id , text = 'حجم دانلود شما ناکافی است برای افزایش حجم اشتراک تهیه کنید')
                                        
                                        elif media == 'MessageMediaType.AUDIO'  :
                                                file_size  = math.ceil(msg.audio.file_size  / (1024*1024))
                                                file_name = str(random.randint(999 , 9999)) + msg.audio.file_name
                                                volume = user.get_sub().re_volum

                                                if int(volume)  > file_size : 
                                                        client.download_media(msg ,file_name=base_dir + f'/downloads/{file_name}')
                                                        user.get_sub().decrease(file_size) 

                                                        client.send_audio(chat_id='me' , audio = base_dir + f'/downloads/{file_name}' , caption=msg.caption)
                                                        if os.path.exists(base_dir + f'/downloads/{file_name}'):
                                                                os.remove(base_dir + f'/downloads/{file_name}')
                                                        edit_message(chat_id=user_id , message_id=message_id , text = '✅ با موفقیت انجام شد ')
                                                        link_data.is_complete = True
                                                        link_data.save()
                                                else :send_message(chat_id=user_id , text = 'حجم دانلود شما ناکافی است برای افزایش حجم اشتراک تهیه کنید')
                                        





                                        elif media == 'MessageMediaType.VOICE' : 
                                                file_size  = math.ceil(msg.voice.file_size  / (1024*1024))
                                                file_name = str(random.randint(999 , 9999)) + '.' +msg.voice.mime_type.split('/')[1]
                                                volume = user.get_sub().re_volum

                                                if int(volume)  > file_size : 
                                                        client.download_media(msg ,file_name=base_dir + f'/downloads/{file_name}')
                                                        user.get_sub().decrease(file_size) 

                                                        client.send_voice(chat_id = 'me' , voice=base_dir + f'/downloads/{file_name}' , caption=msg.caption)
                                                        if os.path.exists(base_dir + f'/downloads/{file_name}'):
                                                                os.remove(base_dir + f'/downloads/{file_name}')
                                                        edit_message(chat_id=user_id , message_id=message_id , text = '✅ با موفقیت انجام شد ')
                                                        link_data.is_complete = True
                                                        link_data.save()
                                                else :send_message(chat_id=user_id , text = 'حجم دانلود شما ناکافی است برای افزایش حجم اشتراک تهیه کنید')
                                                
                                        elif media == 'MessageMediaType.STICKER' : 
                                                file_size  = math.ceil(msg.sticker.file_size  / (1024*1024))
                                                file_name = str(random.randint(33333 , 3333333333)) + msg.sticker.file_name
                                                volume = user.get_sub().re_volum
                                                if int(volume)  > file_size : 
                                                        client.download_media(msg ,file_name=base_dir + f'/downloads/{file_name}')
                                                        user.get_sub().decrease(file_size) 

                                                        client.send_sticker(chat_id = 'me' , sticker=base_dir + f'/downloads/{file_name}' )
                                                        if os.path.exists(base_dir + f'/downloads/{file_name}'):
                                                                os.remove(base_dir + f'/downloads/{file_name}')
                                                        edit_message(chat_id=user_id , message_id=message_id , text = '✅ با موفقیت انجام شد ')
                                                        link_data.is_complete = True
                                                        link_data.save()
                                                else :send_message(chat_id=user_id , text = 'حجم دانلود شما ناکافی است برای افزایش حجم اشتراک تهیه کنید')
                                else : 
                                        try :
                                                msg.copy('me')
                                                edit_message(chat_id=user_id , message_id=message_id , text = '✅ با موفقیت انجام شد ')
                                                link_data.is_complete = True
                                                link_data.save()

                                        except :pass
                        try :
                            client.disconnect()
                        except :pass
                except AuthKeyUnregistered as e :
                        print(e)
                        send_message(chat_id=user_id , text = 'حساب شما به ربات متصل نیست لطفا از طریق دکمه اتصال اقدام کنید')
                        try :
                                client.disconnect()
                        except :pass
                except Exception as e:
                        print(e)
                        try :
                                client.disconnect()
                        except :pass
                finally:
                        try :
                                client.disconnect()
                        except :pass
    except Exception as e:
                try :
                        client.disconnect()
                except :pass

    
                


























        










def send_message(chat_id , text ):
        
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        payload = {'chat_id': chat_id,'text': text}
        response = requests.post(url, data=payload )

def edit_message(chat_id, message_id, text):

    url = f'https://api.telegram.org/bot{bot_token}/editMessageText'
    payload = {'chat_id': chat_id, 'message_id': message_id, 'text': text}
    response = requests.post(url, data=payload)






