from pyrogram import Client, filters
from pyromod import listen
from config import db , api_hash , api_id , proxy , backup_channel
from utils import filters as f
from utils import btn , txt
from sessions.forgram_worker import downloader
import time



@Client.on_message(filters.private & filters.create(f.user_is_active) &filters.create(f.user_is_join) , group=3)
async def manager_user_links (client, message):
    if message.text :
        if message.text.startswith('tg://openmessage?'):
            msg_data = message.text.replace('tg://openmessage?' , '').split('&')
            if len(msg_data) == 2 :
                user_id = msg_data[0].replace('user_id=' ,'')
                message_id = msg_data[1].replace('message_id=' ,'')
                print(user_id)
                print(message_id)
    if message.text  :
        print('if 1' ,message.text)
        if message.text.startswith('tg://openmessage?'):
            msg_data = message.text.replace('tg://openmessage?' , '').split('&')
            if len(msg_data) == 2 :
                user_id = msg_data[0].replace('user_id=' ,'')
                message_id = msg_data[1].replace('message_id=' ,'')
                message.text = f'https://t.me/{str(user_id)}/{str(message_id)}'

        if message.text.startswith('https://t.me/'):
            print('if 2 ',message.text)


            user = db.User.objects.get(username = message.from_user.id )
            if user.session.first() != None :
                if user.get_sub()  != None :
                    if user.get_sub().re_volum >0 :



                        forgram = db.ForGramModel.objects.first()
                        data = await message.reply_text(txt.processing_file, quote=True)
                        time.sleep(1)
                        downloader.apply_async(
                        (message.chat.id, message.text , data.id))
                        db.ForGramUserLinkModel(user = user , forgram = forgram , link = message.text).save()




                    else :await message.reply_text(txt.no_remaining_volum, quote=True)
                else :await message.reply_text(txt.no_active_sub, quote=True)
            else :await message.reply_text(txt.no_active_session, quote=True)
