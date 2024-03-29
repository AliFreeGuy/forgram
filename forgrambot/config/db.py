import sys
import os
import django

sys.dont_write_bytecode = True
script_path = os.path.dirname(__file__)
project_dir = os.path.abspath(os.path.join(script_path, '..','..', '..','web'))
print(project_dir)
print(project_dir)
sys.path.insert(0, project_dir)
os.environ['DJANGO_SETTINGS_MODULE']='web.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()



from accounts.models import User
from forgram.models import ForGramUserMessageModel , ForGramModel , ForGramUsersModel  ,ForGramSettingModel , ForgramPlansModel , ForGramRefUsers , ForgramUserInvoiceModel , ForGramPaymentHistoryModel ,ForGramUserSession  , ForGramUserLinkModel , ForGramGiftModel , ForGramUseGift , SubForGramUserModel , ForGramForwarderAdvanceModel