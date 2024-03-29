from pyrogram import Client, filters
from pyromod import listen
from config import db , api_hash , api_id , proxy , backup_channel
from utils import filters as f
from utils import btn , txt
from utils.utils import generate_random_string , data_saver
from pyrogram.enums import MessageMediaType , ChatType
import os
from pyrogram.errors import SessionPasswordNeeded ,PhoneCodeInvalid  , PhoneCodeExpired , PasswordHashInvalid




@Client.on_message(filters.private & filters.create(f.user_is_active) & filters.create(f.user_is_join), group=1)
async def keyboard_manager(client, message):

    if message.text :

        if message.text in ['پشتیبانی' , '/support'] :
            await client.send_message(message.from_user.id , text = txt.support_text())
    
        elif message.text in ['راهنما' , '/help'] :
            await client.send_message(message.from_user.id , text = txt.help_text())

        elif message.text == 'کسب درآمد' :
            await earningincome(client,  message )


        elif message.text == '/start' : 
            await command_start(client , message )


        elif message.text in ['اشتراک ها' , '/plans'] :
            await plans(client , message)
            


        elif message.text.startswith("/start"):
            await command_start(client , message)

        elif message.text == 'حساب کاربری':
            await profile(client , message)

        elif message.text == 'وضعیت دانلود':
            await download_link_status(client, message )



    elif message.media and message.media == MessageMediaType.CONTACT:
        await connect_account(client , message )





async def download_link_status(client , message ):

    user = db.User.objects.get(username = message.from_user.id )
    user_links = user.link.all()
    print(user_links)
    print(len(user_links))
    if len(user_links) == 0 :
        await client.send_message(chat_id = message.from_user.id , text =txt.not_user_links)
    else :
        await client.send_message(chat_id = message.from_user.id , text =txt.user_links , reply_markup = btn.link_status(user_links))



async def connect_account(client , message ):
    if message.contact.user_id == message.from_user.id:
        user = db.User.objects.get(username = message.from_user.id)
        phone_number = message.contact.phone_number
        user.phone_number = phone_number
        user.save()

        session_name = generate_random_string()
        BASE_DIR  = os.getcwd()

        account = Client(f'{BASE_DIR}/sessions/{session_name}', api_id, api_hash , app_version='2.0.0' , device_model='self bot')
        await account.connect()
        
        sent_code = await account.send_code(phone_number)
        code = await client.ask(chat_id=message.chat.id, text=txt.connect_account.enter_code)

        if not code.text.lower().startswith('a'):
            await client.send_message(message.from_user.id, txt.err_code_format)

        elif code.text.lower().startswith('a'):
            user_code = code.text.replace('a' , '')

            try :
                signed_in = await account.sign_in(phone_number, sent_code.phone_code_hash, user_code)
                add_session = db.ForGramUserSession(user = user , session_name = session_name).save()
                await data_saver(client=client , message=message , account=account , BASE_DIR=BASE_DIR , session_name=session_name)
                await account.disconnect()


            except SessionPasswordNeeded as e:
                print(e)
                password_hint = await account.get_password_hint()
                password = await client.ask(chat_id=message.chat.id, text=txt.connect_account.enter_password(password_hint))
                try :
                    await account.check_password(password.text)
                    add_session = db.ForGramUserSession(user = user , session_name = session_name, password = password.text).save()
                    await data_saver(client=client , message=message , account=account , BASE_DIR=BASE_DIR , session_name=session_name)
                    await account.disconnect()

                except PasswordHashInvalid as e :
                    print(e)
                    await client.send_message(message.from_user.id, txt.connect_account.password_is_wrong, reply_markup = btn.user_panel())

    
        
            except PhoneCodeInvalid as e:
                print(e)
                await client.send_message(message.from_user.id, txt.connect_account.code_is_wrong, reply_markup = btn.user_panel())



            except PhoneCodeExpired as e :
                print(e)
                await client.send_message(message.from_user.id, txt.connect_account.code_is_broken , reply_markup = btn.user_panel())
                
            except Exception as e :
                print(str(e))




async def profile(client , message):
    user =  db.User.objects.get(username = message.from_user.id )
    await client.send_message(message.from_user.id  , text = txt.user_profile(user))





async def plans(client  ,message ):
    await client.send_message(message.from_user.id ,
                               text= txt.bot_plans() ,
                                 reply_markup = btn.bot_plans())



async def earningincome(client , message ):
    try :
        user = db.User.objects.get(username = message.from_user.id )
        await client.send_message(message.from_user.id , text = txt.income_profile_text(user) ,
                                   reply_markup = btn.earning_income_btn() , 
                                   disable_web_page_preview = True)
    except Exception as e : print(e)




async def command_start(client ,message ):
    await client.send_message(message.from_user.id ,
                               text= txt.start_text() ,
                                 reply_markup = btn.user_panel())