from pyrogram import Client, filters
from pyromod import listen
from config import db
from utils import filters as f
from utils import btn , txt















@Client.on_callback_query(filters.create(f.private_call) &filters.create(f.user_is_active)&filters.create(f.user_is_join), group=1)
async def call_entry(client , call   ):

    
    router = call.data.split(':')[0]
    

    if router == 'plans':
        await show_plan(client , call )

    elif router== 'back_to_income' :
        await back_to_income(client , call )   

    elif router == 'settlement' :
        await settlement(client ,call)






async def settlement(client , call ):
    try:
        payment_history_id = call.data.split(':')[2]  # به جای 5 ایدی مورد نظر خود را بگذارید
        payment_history = db.ForGramPaymentHistoryModel.objects.filter(id=payment_history_id)
        if payment_history.exists():
            payment_history = db.ForGramPaymentHistoryModel.objects.get(id = payment_history_id)
            note = await client.ask(chat_id=call.from_user.id, text="لطفاً یادداشت خود را وارد کنید.")
            if note.text:
                payment_history.notes = note.text
            else:
                await alert(client, call, msg="خطا: یادداشت نمی‌تواند خالی باشد.")
            payment_history.is_paid = True
            payment_history.save()
            user = payment_history.user
            amount = payment_history.amount
            try :
                payed = '✅ پرداخت شد'
                await client.edit_message_text(call.from_user.id , message_id=call.message.id ,text = f'{txt.settlementـrequest(user = user , amount=amount)} \n {payed}' ,
                                   reply_markup = btn.settlementـrequest(payment_history.id) , 
                                   disable_web_page_preview = True)
                
                # send messega for pyied amount with admin 
            except :pass
    except Exception as e:
        print(e)





async def back_to_income(client, call ):
    try :
        user = db.User.objects.get(username = call.from_user.id )
        await client.edit_message_text(call.from_user.id , message_id=call.message.id ,text = txt.income_profile_text(user) ,
                                   reply_markup = btn.earning_income_btn() , 
                                   disable_web_page_preview = True)
    except Exception as e : print(e)




async def show_plan(client ,call ):
    plan = db.ForgramPlansModel.objects.filter(id = int(call.data.split(':')[1]))
    if plan.exists :
        plan = plan[0]
        try:
            await client.edit_message_text(call.from_user.id , message_id=call.message.id ,
                                        text = plan.description , 
                                        reply_markup = btn.bot_plans())
        except :pass
    


async def alert(clietn , call  , msg= None ):
    if msg is not None :
        return await call.answer(msg, show_alert=True)
    return await call.answer('خطا لطفا دوباره تلاش کنید !', show_alert=True)

