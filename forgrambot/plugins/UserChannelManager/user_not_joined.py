from pyrogram import Client, filters
from pyromod import listen
from utils import filters as f
from pyrogram.types import ReplyKeyboardRemove
from utils import txt



# @Client.on_message(filters.private &filters.create(f.user_not_joined_channel)  , group=2)
# async def user_not_in_channel(client, message):
#     await client.send_message(chat_id = message.from_user.id , text =txt.user_not_joined() , reply_markup = ReplyKeyboardRemove())




# @Client.on_callback_query(filters.create(f.private_call) &filters.create(f.user_not_joined_channel)  , group=3)
# async def call_user_not_in_channel(client, message):
#     await client.send_message(chat_id = message.from_user.id , text =txt.user_not_joined() , reply_markup = ReplyKeyboardRemove())

