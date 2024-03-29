from config import api_id ,api_hash , bot_token , proxy , plugins
from pyrogram import Client
from pyromod import listen


bot = Client(
        name = "bot",
            api_id=api_id , 
            api_hash=api_hash , 
            bot_token=bot_token , 
#            proxy=proxy ,
            plugins=plugins)


if __name__ == '__main__' : 
 
    bot.run()



        
