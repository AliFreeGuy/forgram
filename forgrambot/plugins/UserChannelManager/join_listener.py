from pyrogram import Client, filters
from pyromod import listen
from config import db
from utils import filters as f
from utils import txt ,btn



@Client.on_chat_member_updated(filters.create(f.channel_join))
async def join_listener(client, message):
    # print(message.new_chat_member)
    # print(message.old_chat_member)


    if message.new_chat_member :
        await user_joined(client , message )
    
    # elif message.old_chat_member :
    #     await user_leaved(client , message )

    


async def  user_joined(client , message ):
    user = db.User.objects.filter(username = message.from_user.id)
    if user.exists() :
        # is_ref = db.ForGramRefUsers.objects.filter(invited_user = user[0])
        # if is_ref.exists():
        await client.send_message(message.from_user.id ,
                               text= txt.start_text() ,
                                 reply_markup = btn.user_panel())


# async def user_leaved(client , message ):
#     print('user leaved ')