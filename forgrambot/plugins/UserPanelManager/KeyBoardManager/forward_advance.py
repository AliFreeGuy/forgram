from pyrogram import Client, filters
from pyromod import listen
from config import db , api_hash , api_id , proxy , backup_channel
from utils import filters as f
from utils import btn , txt
from utils.utils import generate_random_string , data_saver
from pyrogram.enums import MessageMediaType , ChatType
import os
from pyrogram.errors import SessionPasswordNeeded ,PhoneCodeInvalid  , PhoneCodeExpired , PasswordHashInvalid




@Client.on_message(filters.private & filters.create(f.user_is_active) & filters.create(f.user_is_join), group=2)
async def forward_advance_manager(client, message):
    
    if message.text == 'فور حرفه ای' :
        
        await client.send_message(chat_id = message.from_user.id , text = txt.forward_advance()  , reply_markup = btn.forward_advance(message.from_user.id))