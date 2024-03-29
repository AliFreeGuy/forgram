from pyrogram import Client, filters
from pyromod import listen
from config import db
from utils import filters as f
from utils import btn , txt
from pyrogram.errors import MessageTooLong













@Client.on_callback_query(filters.create(f.private_call) & filters.create(f.user_is_active)&filters.create(f.user_is_join), group=2)
async def call_entry(client , call   ):
    router = call.data.split(':')
    
    
    if router[0] == 'income' and len(router) >= 2:


        if router[1] == 'help' :
            await income_help(client, call )

        elif router[1] == 'cart_number' :
            await set_cart_number(client , call )
        
        elif router[1] == 'ref_profile' :
            await ref_profile(client ,call )

        elif router[1] == 'checkout' :
            await checkout(client , call )

        elif router[1] == 'checkout_history' :
            await checkout_history(client , call )

        elif router[1] == 'show_info_checkout' :
            await show_info_checkout(client , call )



async def show_info_checkout(client ,call ):
    user = db.User.objects.get(username = call.from_user.id )
    payment_id = call.data.split(":")[2]
    payment  =user.payment_history.filter(id = int(payment_id))
    if payment.exists():
        notes = payment[0].notes
        try :
            await alert(client , call , msg=f'مبلغ : {str(payment[0].amount)} شماره کارت : {str(payment[0].cart_number)}\n{notes if notes is not None else ""}')
        except MessageTooLong :
            if MessageTooLong.CODE == 400  :
                await client.send_message(call.from_user.id , text = f'مبلغ : {str(payment[0].amount)} شماره کارت : {str(payment[0].cart_number)}\n{notes if notes is not None else ""}')
    else :
        await alert(client , call , msg='هیچی پیدا نکردم :(')






async def checkout_history(client , call ):
    user = db.User.objects.get(username = call.from_user.id )
    user_payment  = user.payment_history.all()

    await client.edit_message_text(call.from_user.id , message_id=call.message.id ,
                                        text = txt.checkout_history , 
                                        reply_markup = btn.checkout_history(user_payment))
   
            




async def checkout(client ,call ):
    user = db.User.objects.get(username=call.from_user.id)
    cart_number = user.cart_number
    payment_history = user.payment_history.filter(is_paid = False)
    user_invoice = user.invoice.filter(is_paid = 'unpaid')
    if user_invoice.exists() and cart_number is not None and not payment_history.exists()  :
        forgram = db.ForGramModel.objects.first()
        amount = user.invoice.first().get_total_unpaid()
        add = db.ForGramPaymentHistoryModel.objects.create(user = user , forgram = forgram , amount = amount , cart_number = cart_number)
        admin = db.ForGramSettingModel.objects.get(name = 'admin').setting['chat_id']
        paying_amounts = user.invoice.all()
        for i in paying_amounts :
            if i.is_paid == 'unpaid' :
                i.is_paid = 'paying'
                i.save()
        await client.send_message(chat_id = admin , text = txt.settlementـrequest(amount , user ), reply_markup = btn.settlementـrequest(id =add.id ))
        await alert(client , call , msg=f'درخاست برداشت مبلغ {str(amount)} تومان با موفقیت ثبت شد لطفا تا تایید ادمین صبور باشید')
        
    elif cart_number is None :
        await alert(client , call , msg='لطفا ابتدا شماره کارت خود را ثبت کنید' )
    elif payment_history.exists() :
        await alert(client ,call , msg='کاربر عزیز شما یک درخاست تسویه حساب پرداخت نشده دارید لطفا بعد از تکمیل درخاست قبلی اقدام کنید')
    elif not user_invoice.exists() :
        await alert(client , call , msg='درامد تسویه نشده شما 0 تومنه :(' )


        



async def income_help(client , call ) :
    try :
        await client.edit_message_text(call.from_user.id , message_id=call.message.id ,
                                        text = txt.incomeـrulesـandـhelp() , 
                                        reply_markup = btn.earning_income_btn())
        
    except :pass






async def ref_profile(client , call ):
    try :
        user = db.User.objects.get(username = call.from_user.id )
        await client.edit_message_text(call.from_user.id , message_id=call.message.id ,
                                        text = txt.income_profile_text(user) , 
                                        reply_markup = btn.earning_income_btn() , disable_web_page_preview = True)
    except :pass






async def set_cart_number(client , call ):
    cart_number = None 
    try :
        await client.delete_messages(chat_id=call.from_user.id,message_ids=call.message.id)
        user = db.User.objects.get(username = call.from_user.id)
        cart_number = await client.ask(chat_id = call.from_user.id  , text = txt.get_cart_number())
        if cart_number.text :
            if cart_number.text == '/cancel' :
                await alert(client , call , msg= 'عملیات با موفقیت کنسل شد')
                await client.send_message(call.from_user.id , text = txt.income_profile_text(user) ,
                                   reply_markup = btn.earning_income_btn() , 
                                   disable_web_page_preview = True)
                

            elif len(cart_number.text) <64 :
                user.cart_number = cart_number.text
                user.save()
                await client.send_message(call.from_user.id , text = txt.income_profile_text(user) ,
                                   reply_markup = btn.earning_income_btn() , 
                                   disable_web_page_preview = True)
            else :
                await alert(client , call , msg= 'خطا : طول شماره کارت ارسالی طولانی است')
                await client.send_message(call.from_user.id , text = txt.income_profile_text(user) ,
                                   reply_markup = btn.earning_income_btn() , 
                                   disable_web_page_preview = True)
        else :

            await alert(client , call )
            await client.send_message(call.from_user.id , text = txt.income_profile_text(user) ,
                                   reply_markup = btn.earning_income_btn() , 
                                   disable_web_page_preview = True)
    except Exception as e :
        print(e)





async def alert(clietn , call  , msg= None ):
    if msg is not None :
        return await call.answer(msg, show_alert=True)
    return await call.answer('خطا لطفا دوباره تلاش کنید !', show_alert=True)

