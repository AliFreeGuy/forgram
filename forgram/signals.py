from django.db.models.signals import pre_save , post_save
from .models import SubForGramUserModel , ForGramSettingModel , ForgramUserInvoiceModel , ForGramModel , ForGramPaymentHistoryModel , ForGramMessageSenderModel
from django.dispatch import receiver
import requests
from .tasks import send_message_task









@receiver(post_save, sender=ForGramMessageSenderModel)
def print_message_on_save(sender, instance, created, **kwargs):
    if created:
        send_message_task.delay(instance.message)




@receiver(pre_save, sender=ForGramPaymentHistoryModel)
def check_is_paid_change(sender, instance, **kwargs):
    try:
        old_instance = sender.objects.get(id=instance.id)
        if old_instance.is_paid != instance.is_paid:
            if old_instance.is_paid == False and instance.is_paid == True :
                    payment_amount = instance.user.invoice.filter(is_paid = 'paying')
                    for i in payment_amount :
                            i.is_paid = 'paid'
                            i.save()

                    text = f'فاکتور شما به مبلغ {instance.amount} تومان واریز شد \n{instance.notes if instance.notes != None else ""}'
                    send_message(chat_id=instance.user.username  , text = text)
        
    except Exception as e :
        print(e)











from django.db.models.signals import post_save
from django.dispatch import receiver






@receiver(pre_save ,sender = SubForGramUserModel )
def send_congratulatory_message(sender , **kwargs):
    
        instance = kwargs['instance']
        if not instance.pk :
            if instance.plan.tag != 'free' :
                bot_token = instance.forgram.bot_token
                text = ForGramSettingModel.objects.get(name='congratulatory_message')
                send_message(chat_id=instance.user.username, text=f'{text.setting["text"]}\n پلن {instance.plan.name} | حجم {str(instance.plan.volum)}')



        if instance.user.invited_user.first():
                user_sub = SubForGramUserModel.objects.filter(user = instance.user)
                percentage_discounts = ForGramSettingModel.objects.get(name ='percentage_discounts')
                if user_sub.exists():percentage = percentage_discounts.setting['second']
                else :percentage = percentage_discounts.setting['first']
                


                if instance.plan.is_discount :
                    plan_price = instance.plan.price - instance.plan.discount
                    user_income = (percentage / 100) * plan_price
                    is_discount = True
                else :
                    plan_price = instance.plan.price
                    user_income = (percentage / 100) * plan_price
                    is_discount = False


                buyer_user = instance.user
                inviting_user = instance.user.invited_user.first().inviting_user
                plan = instance.plan
                forgram = ForGramModel.objects.first()
                amount = int(user_income)

                invoice = ForgramUserInvoiceModel(user = inviting_user ,
                                                plan = plan ,
                                                forgram = forgram ,
                                                buyer_user = buyer_user ,
                                                amount = amount)
        
                if is_discount == True : invoice.is_discount = True
                invoice.save()
                text = f'💸 مبلغ `{str(amount)}` تومان به کیف پول شما واریز شد'
                send_message(chat_id=inviting_user.username , text = text)
                    

                     
                




def send_message(chat_id , text ):
     
        bot_token = ForGramModel.objects.first().bot_token
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        payload = {'chat_id': chat_id,'text': text}
        response = requests.post(url, data=payload )