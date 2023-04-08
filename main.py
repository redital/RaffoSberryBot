import os
import telebot
from telebot import types
import CoseSegrete

API_TOKEN = CoseSegrete.TOKEN

bot = telebot.TeleBot(API_TOKEN)

mode = "Hub"

@bot.message_handler(commands=['start'])
def start(message):
    markup=types.ReplyKeyboardRemove()

    bot.send_message( message.chat.id,
    """\
    Bot realizzato per il controllo del fantastico RaffoSberry
    Se non sai cosa posso fare digita (o premi) /hub !
    """ , markup)

@bot.message_handler(commands=['help'])
def help(message):
    markup=types.ReplyKeyboardRemove()

    messaggiHelp = {}
    messaggiHelp["Hub"] = """\
    Bot realizzato per il controllo del fantastico RaffoSberry.
    Adesso ti trovi nell'hub, digita (o premi) /media per entrare nella modalità media in cui portrai visualizzare i media presenti in una evenutale periferica collegata e riprorne il contenuto
    """
    messaggiHelp["Media"] = """\
    Bot realizzato per il controllo del fantastico RaffoSberry.
    Adesso ti trovi in modalità media in cui portrai visualizzare i media presenti in una evenutale periferica collegata e riprorne il contenuto. 
    Digita (o premi) /hub per tornare all'hub
    """

    bot.send_message( message.chat.id, messaggiHelp[mode], reply_markup=markup )

    
@bot.message_handler(commands=['hub'])
def hub(message):
    markup=types.ReplyKeyboardRemove()

    if mode == "Hub":
        bot.send_message( message.chat.id,
        """\
        Sei già nell'hub
        """ , markup)
    else:
        bot.send_message( message.chat.id,
        """\
        Adesso sei nell'hub. 
        Se non sai cosa fare qui usa l'help!
        """ , markup)
    
@bot.message_handler(commands=['media'])
def media(message):
    markup=types.ReplyKeyboardRemove()

    if mode == "media":
        bot.send_message( message.chat.id,
        """\
        Sei già in modalità media
        """ , markup)
    elif mode != "hub":
        bot.send_message( message.chat.id,
        """\
        Solo dall'hub si può cambiare modalità
        """ , markup)
    else:
        bot.send_message( message.chat.id,
        """\
        Adesso sei in modalità media. 
        Se non sai cosa fare qui usa l'help!
        """ , markup)





@bot.message_handler(func=lambda message: True)
def echo_message(message):
    markup=types.ReplyKeyboardRemove()
    body = '{message}\n' \
           '--\n' \
           '{first}, {last}\n' \
           '{username}, {id}'.format(message=message.text, first=message.from_user.first_name,
                                     last=message.from_user.last_name, username=message.from_user.username,
                                     id=message.chat.id)

    bot.reply_to(message, "Mi dispiace ma non conosco questo comando" , reply_markup=markup)


#bot.polling()
bot.polling(none_stop=True)