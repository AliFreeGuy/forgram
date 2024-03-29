from config import db 
from persiantools.jdatetime import JalaliDate




user_not_have_number = 'حساب شما به ربات متصل نیست لطفا از طریق دکمه اتصال حساب خود را به ربات متصل کنید'
user_does_not_have_advance_plan = 'کاربر عزیز برای استفاده از امکانات فوروارد حرفه ای باید اشتراک حرفه ای داشته باشید'
checkout_history = 'تاریخچه پرداختی های کاربر'
err_code_format = 'فورمت ارسال کد اشتباهه لطفا دوباره بر روی اتصال بزنید و کد را طبق توضیحات ارسال کنید'
no_active_session = 'اکانت شما به ربات متصل نشده است ابتدا بر روی دکمه اتصال بزنید و اکانت خود را به ربات متصل کنید برای اطلاعات بیشتر بر رویه راهنما یا /help بزنید'
no_active_sub = 'شما اشتراک فعالی ندارید برای فعال سازی اشتراک بر روی دکمه اشتراک ها یا /plans بزنید و اشتراک مورد نظر خود را فعال کنید'
no_remaining_volum = 'حجم شما به پایان رسیده لطفا برای افزایش حجم بر روی دکمه اشتراک ها یا /plans بزنید'
processing_file = 'در حال پردازش لطفا صبور باشید ...'
not_user_links ='شما هیچ لینکی برای فوروارد ارسال نکردید برای فوروارد باید لینک پست مورد نظر خود را به ربات ارسال کنید'
user_links = 'لیست لینک های ارسال شده شما به ربات'
giftـexpired = 'کد هدیه منقضی شده دیر اومدی :('
gift_not_valid = '🧐 همچین کد هدیه ای نداریم '
duplicate_gift = '👀 کد هدیه یک بار مصرفه شما قبلا استفاده کردید از این هدیه '
you_have_sub = '🎟 شما اشتراک فعال دارید'
wait_message = 'در حال بررسی لطفا صبور باشید ...'
err_set_channel = 'خطا لطفا دوباره تلاش کنید'
account_dont_connect = 'حساب شما به ربات متصل نیست لطفا بر روی اتصال حساب بزنید و حساب خود را به ربات متصل کنید'
source_channel_not_set = 'کانال مبدا خالی است'
destination_channel_not_set = 'کانال مقصد خالی است'
not_has_media = 'حدقل باید یک نوع از پست مجاز باشد'





def gift_used(volum):
    return f'🥳 تبریک مقدار {str(volum)} مگابایت هدیه برای شما فعال شد'



class ConnectAccount :

    @property
    def enter_code(self):
        text = '''
کد به حساب تلگرام شما ارسال شد .
قبل از کد حرف a را بنویسید برای مثال اگر کد شما 12345 است کد را به این شکل برای ربات ارسال کنید  :  `a12345`'''
        return text



    @property
    def code_is_wrong(self):
        return '''کد وارد شده اشتباه است لطفا دوباره بر روی دکمه اتصال بزنید و کد را طبق توضیحات و درست وارد کنید.'''
    

    @property
    def password_is_wrong(self):
        return 'پسورد وارد شده اشتباه است برای ورود به اکانت مجددا بر روی اتصال بزنید و دوباره تلاش کنید'


    @property
    def code_is_broken(self):
        return 'کد وارد شده منقضی شده برای ورود به اکانت مجددا بر روی اتصال بزنید و دوباره تلاش کنید'


    @property
    def logined_successfully(self):
        return 'اکانت شما با موفقیت به ربات متصل شد'
    

    def enter_password(self , password_hint):
        return f'پسورد دو مرحله ای خود را وارد کنید :\n `{password_hint}`'

    


connect_account = ConnectAccount()













def forward_worker_info(instance):
    if instance.type == 'allposts':
        text = f'''
فوروارد همه پست ها از کانال `{instance.source_channel or 'خالی'}`  به کانال  `{instance.destination_channel or 'خالی'}`

حساب متصل به ربات : `{instance.user.username if instance.session_name else 'خالی'}`

پست های مجاز:

'''


    elif instance.type == 'momentary':
        text = f'''
فوروارد لحظه‌ای از کانال `{instance.source_channel or 'خالی'}`  به کانال  `{instance.destination_channel or 'خالی'}`

حساب متصل به ربات : `{instance.user.username if instance.session_name else 'خالی'}`

پست های مجاز:

'''


    media_checks = [f'{"✔️" if getattr(instance, media, False) else "❌"} - {media_display_name}'
                        for media, media_display_name in [('text', 'Text'), ('photo', 'Photo'), ('audio', 'Audio'),
                                                          ('document', 'Document'), ('sticker', 'Sticker'), ('video', 'Video'),
                                                          ('animation', 'Animation'), ('voice', 'Voice'), ('video_note', 'Video Note')]
                        ]
    text += '\n'.join(media_checks)
    return text





def forward_advance():
    data = db.ForGramSettingModel.objects.filter(name = 'forward_advance_info').exists()
    if data :
        return db.ForGramSettingModel.objects.get(name='forward_advance_info').setting['text']
    return 'خالی'





def welcome_text():
     data = db.ForGramSettingModel.objects.filter(name = 'welcome_text')
     if data.exists :
          return data[0].setting['text']
     return 'خالی'


def support_text():
    data = db.ForGramSettingModel.objects.filter(name = 'support_text').exists()
    if data :
        return db.ForGramSettingModel.objects.get(name='support_text').setting['text']
    return 'خالی'

def help_text():
    data = db.ForGramSettingModel.objects.filter(name = 'help_text').exists()
    if data :
        return db.ForGramSettingModel.objects.get(name='help_text').setting['text']
    return 'خالی'


def bot_plans() :
    return 'چه پلنی نیاز داری ؟! '




def start_text():
    return 'منو اصلی ربات برای دسترسی به هر بخش بر روی دکمه مورد نظر خود کلیک کنید'




def income_profile_text(user ):
    users_ref = (len(user.inviting_user.all()))
    total_paid = 0
    total_unpaid = 0
    if user.invoice.first() :
        total_paid = user.invoice.first().get_total_paid()
        total_unpaid = user.invoice.first().get_total_unpaid()
    
    

    text = f'''
آیدی اختصاصی : `{user.username}`

افراد دعوت شده : `{str(users_ref)}`

درآمد تسویه شده  : `{str(total_paid)}`

درآمد تسویه نشده  : `{str(total_unpaid)}`

شماره کارت شما : `{user.cart_number if user.cart_number else "خالی"}`

لینک اختصاصی  : https://t.me/forgram_bot?start=ref_{str(user.username)}

⁉️ برای کسب اطلاعات بیشتر روی دکمه راهنما و قوانین بزنید'''
    return text


def incomeـrulesـandـhelp():
    data = db.ForGramSettingModel.objects.filter(name = 'incomeـrulesـandـhelp').exists()
    if data :
        return db.ForGramSettingModel.objects.get(name='incomeـrulesـandـhelp').setting['text']
    return 'خالی'


def get_ref_link(ref_link):
    data = db.ForGramSettingModel.objects.filter(name = 'ref_link_text').exists()
    if data :
        text = db.ForGramSettingModel.objects.get(name='ref_link_text').setting['text']
        text = f'{text}\n\n🔰 {ref_link}'
        return text
    return 'خالی'






def user_profile(user):
    user_sub = user.get_sub()

    if user_sub:
        sub_name = user_sub.plan.name
        remaining_volume_gb = round((user_sub.volum - user_sub.volum_used) / 1000, 2)
        used_volume_gb = round(user_sub.volum_used / 1000, 2)
        expiry_date = JalaliDate(user_sub.expiry).strftime("%Y-%m-%d") if user_sub.expiry else "نامشخص"
        year, month, day = expiry_date.split('-')
        expiry_date = f'{day}-{month}-{year}'
    else:
        sub_name = 'ندارید'
        remaining_volume_gb = "0"
        used_volume_gb = "0"
        expiry_date = "0"
    

    if user_sub.plan.tag == 'free' :

        expiry_time = ''
    else :
        expiry_time = f'تاریخ پایان اشتراک : `{expiry_date}`'
    text = f'''
آیدی اختصاصی : `{user.username}`
اشتراک فعال : `{sub_name}`
حجم باقی مانده : `{remaining_volume_gb} گیگابایت`
حجم استفاده شده : `{used_volume_gb} گیگابایت`
{expiry_time}

@BLUEBOTS
'''
    return text




def user_not_active():
    support_id  = db.ForGramSettingModel.objects.get(name='support_id').setting['username']
    return f'حساب شما غیر فعال است لطفا برای اطلاعات بیشتر با ادمین @{support_id} در ارتباط باشید'


def code_sent():
    text = '''
کد 5 رقمی برای اتصال ربات به اکانت شما ارسال شد
لطفا کد خود را وارد کن :
'''
    return text




def user_not_joined():
    
    data = db.ForGramSettingModel.objects.filter(name = 'user_not_join').exists()
    if data :
        return db.ForGramSettingModel.objects.get(name='user_not_join').setting['text']
    return 'خالی'


def inviting_user_welcome(first_name):
    text = f'''
🥳 کاربر `{first_name}` با موفقیت با لینک شما در ربات عضو شد
'''
    return text


def settlementـrequest(amount  , user  ):
    text = f'''
درخواست تسویه حساب 

کاربر : `{user.username}`
مبلغ : `{str(amount)}`
شماره کارت : `{user.cart_number}`
'''
    return text


def get_cart_number():
    text = '''
لطفا شماره کارت خود را ارسال کنید 
شماره کارت باید به همراه نام صاحب کارت ارسال شود برای مثال : `6037991785967857 جادی میرمیرانی`
درصورت اشتباه وارد کرد مسولیت آن به عهده خود کاربر میباشد.
لغو : /cancel
'''

    return text

