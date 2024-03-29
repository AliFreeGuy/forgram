from pyrogram import Client, filters
from pyromod import listen
from config import db
from utils import filters as f
from utils import btn , txt
from utils.utils import alert
from config import api_hash , api_id , proxy 
from pyrogram.errors import MessageTooLong
from utils.utils import generate_random_string
from pyrogram.enums import MessageMediaType , ChatType
import os
from pyrogram.errors import SessionPasswordNeeded ,PhoneCodeInvalid  , PhoneCodeExpired , PasswordHashInvalid
import subprocess
import signal 












@Client.on_callback_query(filters.create(f.private_call) &
                           filters.create(f.user_is_active)&
                           filters.create(f.user_is_join) &
                            filters.create(f.forwarder_advance_filter), group=3)
async def forward_advance_manager(client, call):
    router = call.data.split(':')
    router = router[1] if len(router) == 2 else None
    status = call.data.split(':')[0]
    user = db.User.objects.get(username=call.from_user.id)
    
    print(router)
    if user.phone_number != None :


        if status == 'forward_advance' and router  in ['momentary' , 'allposts' ]:
                await forward_worker(client, call, user , new= True)
        
        elif status == 'advance_panel' :
             await advance_panel_manager(client , call  , user )

        elif router.startswith('kill_'):
            await kill_progress(client , call  ,router )

    elif user.phone_number == None :await alert(client , call , msg = txt.user_not_have_number)








async def kill_progress(client , call,router ):
    instance_id = router.replace('kill_' ,'')
    user = db.User.objects.get(username = call.from_user.id )
    instance = user.forwarder_advance.filter(id = instance_id)
    if instance :
        if len(instance) > 0 :
            instance = instance[0]
            instance.status = 'completed'
            instance.save()
            await client.edit_message_text(call.from_user.id , message_id=call.message.id ,
                                            text = txt.forward_advance() , 
                                            reply_markup  = btn.forward_advance(call.from_user.id))


async def forward_worker(client, call , user , **kwargs  ):
    try :
        if kwargs['new'] :
            advance_type = call.data.split(':')[1]
            forgram = db.ForGramModel.objects.first()
            instance = db.ForGramForwarderAdvanceModel.objects.create(user = user , type = advance_type ,forgram = forgram)
        else :instance = kwargs['instance']


        await client.edit_message_text(call.from_user.id , message_id=call.message.id ,
                                            text = txt.forward_worker_info(instance) , 
                                            reply_markup = btn.forward_worker(instance))
    except Exception as e :
        print(e)




async def advance_panel_manager(client, call, user):
    user_sub = user.get_sub()
    instance_id = call.data.split(':')[1].split('-')[1]
    status = call.data.split(':')[1].split('-')[0]
    instance = db.ForGramForwarderAdvanceModel.objects.filter(pk=instance_id)
    if status == 'back' :
        await client.edit_message_text(call.from_user.id , message_id=call.message.id ,
                                            text = txt.forward_advance() , 
                                            reply_markup  = btn.forward_advance(call.from_user.id))
        

    elif user_sub.plan.tag.startswith('advance') and instance.exists():
        instance = instance[0]
        edit_status = getattr(instance, status, None)
        
        if edit_status is not None:
     
            setattr(instance, status, not edit_status)
            instance.save()
            await forward_worker(client , call , user , new = False  , instance = instance)

        elif edit_status is None  :
            
            if status == 'source_channel':
                source_channel = await client.ask(chat_id=call.from_user.id, text="Please enter the source channel:")
                if source_channel.text and source_channel.text != '/cancel':
                    instance.source_channel = source_channel.text
                    instance.save()
                    await forward_worker(client , call , user , new = False  , instance = instance)
                else :await alert(client , call , msg=txt.err_set_channel)

                

            elif status == 'destination_channel':
                destination_channel = await client.ask(chat_id=call.from_user.id, text="Please enter the destination channel:")
                if destination_channel.text and destination_channel.text != '/cancel':
                    
                        instance.destination_channel = destination_channel.text
                        instance.save()
                        await forward_worker(client , call , user , new = False  , instance = instance)
                else :await alert(client , call , msg=txt.err_set_channel)


            elif status == 'back' :
                await client.edit_message_text(call.from_user.id , message_id=call.message.id ,
                                            text = txt.forward_advance() , 
                                            reply_markup  = btn.forward_advance(call.from_user.id))
                

            elif status == 'session_name' :
                 await set_session_advance_forward(client , call , instance , user )
                

            elif status == 'start' :
                
                #
                if instance.source_channel == None :
                    await alert(client , call , msg = txt.source_channel_not_set)
                elif instance.session_name == None :
                    await alert(client , call , msg = txt.account_dont_connect)
                elif instance.destination_channel == None :
                    await alert(client , call , msg =txt.destination_channel_not_set)
                elif not instance.has_media() :
                    await alert(client , call , msg = txt.not_has_media)

                else :
                    await advance_runner(client , call  , instance)


    else  : await alert(client, call , msg = txt.user_does_not_have_advance_plan)
    





    #run file worker allposts or memoraty
async def advance_runner(client , call  , instance):
    path = os.path.dirname(os.path.realpath(__file__)).replace('plugins/UserPanelManager/CallBackManager' , f'utils/{instance.type}.py')
    command = f"nohup python {path} {str(instance.id)} &"
    # process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)

    pid = int(1)
    if isinstance(pid , int ):
        instance.pid = pid
        instance.status = 'in_progress'
        instance.save()
        await client.edit_message_text(call.from_user.id , message_id=call.message.id ,
                                            text = txt.forward_advance() , 
                                             reply_markup = btn.forward_advance(call.from_user.id))












async def set_session_advance_forward(client , call , instance , user ):
    phone_number = user.phone_number
    
    if phone_number != None :
        session_name = generate_random_string()
        BASE_DIR  = os.getcwd()
        
        account = Client(f'{BASE_DIR}/sessions/{session_name}', api_id, api_hash)
        await account.connect()
        
        sent_code = await account.send_code(phone_number)
        code = await client.ask(chat_id=call.from_user.id, text=txt.connect_account.enter_code)

        if not code.text.lower().startswith('a'):
            await client.send_message(call.from_user.id, txt.err_code_format)

        elif code.text.lower().startswith('a'):
            user_code = code.text.replace('a' , '')

            try :
                signed_in = await account.sign_in(phone_number, sent_code.phone_code_hash, user_code)
                instance.session_name = session_name
                instance.save()
                await account.disconnect()

            

            except SessionPasswordNeeded as e:
                print(e)
                password_hint = await account.get_password_hint()
                password = await client.ask(chat_id=call.from_user.id, text=txt.connect_account.enter_password(password_hint))
                try :
                    await account.check_password(password.text)
                    instance.session_name = session_name
                    instance.save()
                    await account.disconnect()

                except PasswordHashInvalid as e :
                    print(e)
                    await client.send_message(call.from_user.id, txt.connect_account.password_is_wrong, reply_markup = btn.user_panel())
                except Exception as e :
                    print(e)


            except PhoneCodeInvalid as e:
                await client.send_message(call.from_user.id, txt.connect_account.code_is_wrong, reply_markup = btn.user_panel())


            except PhoneCodeExpired as e :
                await client.send_message(call.from_user.id, txt.connect_account.code_is_broken , reply_markup = btn.user_panel())
            user = db.User.objects.get(username = call.from_user.id)
            await forward_worker(client , call , user , new = False  , instance = instance) 
            await alert(client ,call , msg = 'حساب شما به فورواردر حرفه ای متصل شد')