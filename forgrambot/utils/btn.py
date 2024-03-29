from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineKeyboardButton , KeyboardButton)
from config import db 







send_phone = ReplyKeyboardMarkup([[KeyboardButton('اتصال حساب به ربات' , request_contact=True)]] , resize_keyboard= True)       




def forward_worker(instance):
    buttons = [
        [
            InlineKeyboardButton(text=f'{"✔️" if instance.video_note else "❌"} Video Note', callback_data=f'advance_panel:video_note-{instance.id}'),
            InlineKeyboardButton(text=f'{"✔️" if instance.text else "❌"} Text', callback_data=f'advance_panel:text-{instance.id}'),
            InlineKeyboardButton(text=f'{"✔️" if instance.photo else "❌"} Photo', callback_data=f'advance_panel:photo-{instance.id}'),
        ],
        [
            InlineKeyboardButton(text=f'{"✔️" if instance.document else "❌"} Document', callback_data=f'advance_panel:document-{instance.id}'),
            InlineKeyboardButton(text=f'{"✔️" if instance.sticker else "❌"} Sticker', callback_data=f'advance_panel:sticker-{instance.id}'),
            InlineKeyboardButton(text=f'{"✔️" if instance.video else "❌"} Video', callback_data=f'advance_panel:video-{instance.id}'),
        ],
        [
            InlineKeyboardButton(text=f'{"✔️" if instance.animation else "❌"} Animation', callback_data=f'advance_panel:animation-{instance.id}'),
            InlineKeyboardButton(text=f'{"✔️" if instance.voice else "❌"} Voice', callback_data=f'advance_panel:voice-{instance.id}'),
            InlineKeyboardButton(text=f'{"✔️" if instance.audio else "❌"} Audio', callback_data=f'advance_panel:audio-{instance.id}'),

        ],
    ]

    marks = [
        [
         InlineKeyboardButton(text=f'کانال مقصد : {instance.destination_channel if instance.destination_channel else "خالی"}', callback_data=f'advance_panel:destination_channel-{instance.id}'),
         InlineKeyboardButton(text=f'کانال مبدا : {instance.source_channel if instance.source_channel else "خالی"}', callback_data=f'advance_panel:source_channel-{instance.id}'),],
        # [],
        *buttons,
        [
        InlineKeyboardButton(text='برگشت', callback_data=f'advance_panel:back-{instance.id}'),
         InlineKeyboardButton(text='اتصال حساب', callback_data=f'advance_panel:session_name-{instance.id}'),
         InlineKeyboardButton(text='شروع', callback_data=f'advance_panel:start-{instance.id}'),
         ],

        # [
        # ],

    ]

    return InlineKeyboardMarkup(marks)






def forward_advance(chat_id):
    user = db.User.objects.get(username = chat_id)
    user_advance_worker = user.forwarder_advance.filter(pid__isnull=False, status='in_progress')[:10]    
    marks = [
        [InlineKeyboardButton(text ='➕ فوروارد لحضه ای', callback_data=f'forward_advance:momentary'),
         InlineKeyboardButton(text ='➕ فوروارد همه پست ها', callback_data=f'forward_advance:allposts')] ,
        
]
    
    if len(user_advance_worker) <= 10 :
    
        for i in user_advance_worker :
            if i.type == 'allposts' :
                name = f'فوروارد همه پست از {i.source_channel}'
            else : name = f'فوروارد لحضه ای از {i.source_channel}'
            marks.append([InlineKeyboardButton(text =name, callback_data=f'forward_advance:kill_{i.id}')] ,)
   

    return InlineKeyboardMarkup(marks)





def link_status(user_links):
    marks = []
    for i in user_links :
        if i.is_complete == False :
            text = f'در حال انجام - {i.link}'
        else :
            text= f'انجام شد - {i.link}'
        marks.append([InlineKeyboardButton(text =text, callback_data=f'link_status:{str(i.id)}')])
    if len(marks) > 20 :
        marks = marks[:20]
    return InlineKeyboardMarkup(marks) 

    


def user_panel():
    marks = [
        ['اشتراک ها','حساب کاربری' ]  , 
        ['فور حرفه ای' , KeyboardButton('اتصال' , request_contact=True),'کسب درآمد'],
         ['پشتیبانی'  , 'وضعیت دانلود','راهنما']  ,
        ]

    return ReplyKeyboardMarkup(marks , resize_keyboard=True , placeholder='لینک پست را وارد کنید ...')



def bot_plans():
    marks = []
    plans = db.ForgramPlansModel.objects.filter(is_active = True).order_by('-id')
    if plans.exists :
        for plan in plans :
            marks.append(InlineKeyboardButton(text =plan.name, callback_data=f'plans:{str(plan.id)}'))
    chunked_list = [marks[i:i+3] for i in range(0, len(marks), 3)]
    try :
        support_id = db.ForGramSettingModel.objects.get(name = 'support_id').setting['username']
        chunked_list.append([InlineKeyboardButton(text ='تهیه اشتراک', url = f'https://t.me/{support_id}')])
    except :pass
    return InlineKeyboardMarkup(chunked_list) 
    
        
    
     
    

def settlementـrequest(id):
    marks = [[InlineKeyboardButton(text ='پرداخت شد', callback_data=f'settlement:was_paid:{id}'),] ,]
    return InlineKeyboardMarkup(marks) 




def earning_income_btn():
    marks = [
        
            [InlineKeyboardButton(text ='اطلاعات حساب کاربری', callback_data=f'income:ref_profile'),] ,

               [InlineKeyboardButton(text = 'درخواست تسویه حساب'  ,callback_data='income:checkout' ),
               InlineKeyboardButton(text= 'تاریخچه تسویه حساب'  ,callback_data=f'income:checkout_history' )],

            [InlineKeyboardButton(text = 'ثبت شماره کارت', callback_data=f'income:cart_number') ,
            InlineKeyboardButton(text ='قوانین و راهنما', callback_data=f'income:help'),] ,

               ]
    return InlineKeyboardMarkup(marks) 



def checkout_history(user_payment):
    marks = []
    
    
    for i in user_payment :
        pending = 'در حال بررسی ...'
        paid = 'پرداخت شد'
        name = f'مبلغ {str(i.amount)} {paid if i.is_paid else pending}'
        marks.append([InlineKeyboardButton(text =name, callback_data=f'income:show_info_checkout:{i.id}'),])
    marks.append([InlineKeyboardButton(text ='برگشت', callback_data=f'back_to_income'),])
    return InlineKeyboardMarkup(marks) 
