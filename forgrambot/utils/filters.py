from pyrogram import filters
import datetime
from config import admin , db 
from pyrogram.enums.chat_type import ChatType







async def private_call(_ , client , call ):
    if call.message.chat.type == ChatType.PRIVATE :
        return True
    return False


async def channel_join(_ , client , message ):
    try :
        channel_id  = int(message.chat.id) 
        channel = int(db.ForGramSettingModel.objects.get(name = 'channel_data').setting['chat_id'])
        if channel_id == channel :
            return True
        else :
            return False
    except :
        return False


async def user_joined_channel(_ , client, message):
    
    user = message.from_user.id 
    channel = db.ForGramSettingModel.objects.get(name = 'channel_data').setting['chat_id']
    try : 
        await client.get_chat_member(int(f'{channel}') , user )
        return True
    except Exception as e : return False




async def user_not_joined_channel(_ , client, message):
    
    user = message.from_user.id 
    channel = db.ForGramSettingModel.objects.get(name = 'channel_data').setting['chat_id']
    try : 
        await client.get_chat_member(int(f'{channel}') , user )
        return False
    except Exception as e : return True




async def user_is_active(_ , client , message ):
    user = db.User.objects.filter(username = message.from_user.id )
    if user.exists():
        user = user[0]
        if user.is_active :
            return True
        else :
            return False
    return True

async def user_not_active(_ , client , message ) :
    user = db.User.objects.filter(username = message.from_user.id )
    if user.exists():
        user = user[0]
        if user.is_active :
            return False
        else :
            return True
    return True





async def user_is_join(_ , client , message ):
    user  = db.User.objects.filter(username = message.from_user.id)
    if user.exists():
        user = user[0]
        user_messages = user.message.all()
        force_join = db.ForGramSettingModel.objects.get(name = 'forced_join')
        force_status = force_join.setting['status']
        force_count= int(force_join.setting['count_message'])
        if force_status == 'True' and len(user_messages) > force_count :
            try :
                channel = db.ForGramSettingModel.objects.get(name = 'channel_data').setting['chat_id']
                await   client.get_chat_member(int(f'{channel}') , message.from_user.id )
                return True
            except :
                return False
        return True
    return True



async def forwarder_advance_filter(_ , client , call ):
    router = call.data.split(':')[0]
    if router in ['forward_advance' , 'advance_panel']:
        return True
    return False


async def user_not_join(_ , client , message ):
    user  = db.User.objects.filter(username = message.from_user.id)
    if user.exists():
        user = user[0]
        user_messages = user.message.all()
        force_join = db.ForGramSettingModel.objects.get(name = 'forced_join')
        force_status = force_join.setting['status']
        force_count= int(force_join.setting['count_message'])

        if force_status == 'True' and len(user_messages) >= force_count :
            try :
                channel = db.ForGramSettingModel.objects.get(name = 'channel_data').setting['chat_id']
                await   client.get_chat_member(int(f'{channel}') , message.from_user.id )
                print('user is join ')
                return False
            except :
                return True
        # 
        return False
      
    return False

# async def user_is_join(_ , client, message):
#     user = db.User.objects.filter(username = message.from_user.id )
#     if user.exists() :
#         user = user[0]
#         user_sub = user.get_sub()
#         user_is_ref = user.invited_user.first()
#         user_links = user.link.filter(is_complete = True)
#         if user_sub != None and user_sub.plan.tag != 'free' or user_is_ref != None or len(user_links)>= 5 :
#             try :
#                 channel = db.ForGramSettingModel.objects.get(name = 'channel_data').setting['chat_id']
#                 await   client.get_chat_member(int(f'{channel}') , message.from_user.id )
#                 return True
#             except :
#                 return False
#         return True
#     return True


# async def user_not_join(_ , client , message ):
#     user = db.User.objects.filter(username = message.from_user.id )
#     print(user)
#     if user.exists() :
#         user = user[0]
#         user_sub = user.get_sub()
#         user_is_ref = user.invited_user.first()
#         user_links = user.link.filter(is_complete = True)
#         if user_sub != None and user_sub.plan.tag != 'free' or user_is_ref != None or len(user_links)>= 5 :
#             try :
#                 channel = db.ForGramSettingModel.objects.get(name = 'channel_data').setting['chat_id']
#                 await   client.get_chat_member(int(f'{channel}') , message.from_user.id )
#                 return False
#             except :
#                 return True
#         return True
#     return True