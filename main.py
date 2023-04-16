import telebot
from telebot import types
import CoseSegrete
import DeviceNavigation

API_TOKEN = CoseSegrete.TOKEN

bot = telebot.TeleBot(API_TOKEN)

DeviceNavigation.init()

mode = "Hub"

@bot.message_handler(commands=['start'])
def start(message):
    markup=types.ReplyKeyboardRemove()

    bot.send_message( 
        message.chat.id,
        """\
Bot realizzato per il controllo del fantastico RaffoSberry
Se non sai cosa posso fare digita (o premi) /help !
        """, 
        reply_markup=markup)

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

    bot.send_message(message.chat.id, messaggiHelp[mode], reply_markup=markup)

    
@bot.message_handler(commands=['hub'])
def hub(message):
    global mode
    markup=types.ReplyKeyboardRemove()

    if mode == "Hub":
        bot.send_message( 
            message.chat.id,
            "Sei già nell'hub", 
            reply_markup=markup
            )
    else:
        mode = "Hub"
        bot.send_message(
            message.chat.id,
            "Adesso sei nell'hub.\nSe non sai cosa fare qui usa l'help!", 
            reply_markup=markup
            )
        DeviceNavigation.backHome()
    
@bot.message_handler(commands=['media'])
def media(message):
    global mode
    markup=types.ReplyKeyboardRemove()

    if mode == "Media":
        bot.send_message( 
            message.chat.id,
            "Sei già in modalità media", 
            reply_markup=markup
            )
    elif mode != "Hub":
        bot.send_message( 
            message.chat.id,
            "Solo dall'hub si può cambiare modalità", 
            reply_markup=markup
            )
    else:
        mode="Media"
        bot.send_message(
            message.chat.id,
            "Adesso sei in modalità media.\nSe non sai cosa fare qui usa l'help!", 
            reply_markup=markup
            )

def isMediaModeHandler(message):
    if mode != "Media":
        bot.send_message( 
            message.chat.id,
            "Comando disponibile solo in modalità media"
            )
    return mode == "Media"

@bot.message_handler(commands=['dispositivi'])
def dispositivi(message):
    markup=types.ReplyKeyboardRemove()
    
    if not isMediaModeHandler(message):
        return
    
    devices, devicesText = DeviceNavigation.getUsbDevices()
    if len(devices) == 0:
        bot.send_message(
            message.chat.id,
            "Non ci sono dispositivi collegati",
            reply_markup=markup
            )
    else:
        bot.send_message( 
            message.chat.id,
            devicesText, 
            reply_markup=markup
            )
    
@bot.message_handler(commands=['selezionaDispositivo'])
def dispositivi(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    if not isMediaModeHandler(message):
        return
    
    DeviceNavigation.backHome()
    devices = DeviceNavigation.getUsbDevices()[0]
    if len(devices) == 0:
        bot.send_message(
            message.chat.id,
            "Non ci sono dispositivi collegati",
            reply_markup=markup
            )
    else:
        for device in devices:
            markup.add(device["NAME"])
        msg = bot.send_message(
                message.chat.id,
                "Che dispositivo vuoi esplorare?",
                reply_markup=markup
                )
    
    bot.register_next_step_handler(msg, getDeviceSelection)
    
def getDeviceSelection(message):
    selection = -1
    devices = DeviceNavigation.getUsbDevices()[0]
    for i in range(len(devices)):
        if message.text == devices[i]["NAME"]:
            selection = i
            break
    DeviceNavigation.deviceSelection(devices,selection)

    return "stocazzo"




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