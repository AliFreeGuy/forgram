from pyrogram import Client, filters
from pyromod import listen
from config import db
from utils.decorators import user_updater
from pyrogram.types import ReplyKeyboardRemove
from utils import filters as f
from utils import btn , txt
from utils.utils import user_is_join
from plugins.UserPanelManager.KeyBoardManager.keyboard_manager import command_start




@Client.on_message(filters.private & filters.create(f.user_is_active) &filters.create(f.user_is_join) , group=0)
@user_updater
async def message_entry(client, message, user=None):
    user_is_created = True if len(user.message.all()) == 1 else False
    if message.text and message.text.startswith("/start ref_") :
        if user_is_created :
            inviter_username = message.text.replace('/start ref_' , '')
            if len(inviter_username) > 5 :

                inviting_user= db.User.objects.get(username = message.text.replace('/start ref_' , ''))
                invited_user = db.User.objects.get(username = message.from_user.id)
                is_invite = db.ForGramRefUsers.objects.filter(invited_user = invited_user , inviting_user = inviting_user).exists()
                
                if not is_invite  :
                    
                    db.ForGramRefUsers.objects.create(inviting_user= inviting_user , invited_user = invited_user)
                    await client.send_message(int(inviting_user.username) , text = txt.inviting_user_welcome(message.from_user.first_name))
    
            
    elif message.text and message.text.startswith("/start gift_"):
        gift_code = message.text.replace('/start gift_' , '')
        gift = db.ForGramGiftModel.objects.filter(code = gift_code)
        user = db.User.objects.get(username = message.from_user.id)
        if gift.exists() :
            gift = gift[0]
            if gift.used <= gift.count :
                check = user.gift.filter(gift = gift )
                if not check.exists():
                    user_sub = user.get_sub()
                    if user_sub is not None and user_sub.plan.tag == 'free' :
                        add_gift = db.ForGramUseGift(user = user , gift = gift)
                        add_gift.save()
                        user_sub.volum += gift.volum
                        user_sub.save()
                        gift.used +=1
                        gift.save()
                        await client.send_message(message.from_user.id , text = txt.gift_used(gift.volum))

                    else :await client.send_message(message.from_user.id , text =txt.you_have_sub)
                else :await client.send_message(message.from_user.id , text = txt.duplicate_gift)
            else :await client.send_message(message.from_user.id , text =txt.giftـexpired)
        else :await client.send_message(message.from_user.id , text = txt.gift_not_valid)


 



@Client.on_callback_query(filters.create(f.private_call)&filters.create(f.user_is_join), group=0)
@user_updater
async def call_entry(client , message , user  ):
    pass
    


@Client.on_message(filters.private & filters.create(f.user_is_active) &filters.create(f.user_not_join) , group=0)
@user_updater
async def user_not_join(client , message  ,user):
    await client.send_message(message.from_user.id , text = txt.user_not_joined() , reply_markup = ReplyKeyboardRemove())






@Client.on_message(filters.private & filters.create(f.user_not_active) &filters.create(f.user_is_join), group=0)
@user_updater
async def user_not_active_manager(client , message  , user ):
    await client.send_message(message.from_user.id , text = txt.user_not_active() , reply_markup = ReplyKeyboardRemove())
