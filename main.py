import telebot
from telebot import types
import CoseSegrete
import DeviceNavigation
import VLCHandler
import os
from vlc import State

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
        VLCHandler.setUp()
        bot.send_message(
            message.chat.id,
            "Adesso sei in modalità media.\nSe non sai cosa fare qui usa l'help!", 
            reply_markup=markup
            )
        
def isMediaMode():
    return mode=="Media"

def isMediaModeHandler(message):
    if not isMediaMode():
        bot.send_message( 
            message.chat.id,
            "Comando disponibile solo in modalità media"
            )
    return isMediaMode()

#=============================================================================================================================================
#                                                   Navigazione nel file system
#=============================================================================================================================================


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
            reply_markup=types.ReplyKeyboardRemove()
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
    inCartella(message)
    
def inCartella(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    mediaText, mediaList = DeviceNavigation.displayMedia()
    markup.add("Esplora","Torna")
    if len(mediaList) == 0:
        markup.add("Annulla")
        msg = bot.send_message(
            message.chat.id,
            "Non ci sono media in questa cartella\nVuoi esplorare il file system?",
            reply_markup=markup
            )
        bot.register_next_step_handler(msg, esplora)
    else:
        for file in mediaList:
            markup.add(file)
        msg = bot.send_message(
            message.chat.id,
            mediaText + "\nScegli il file da riprodurre, oppure Esplora se vuoi esplorare il file system",
            reply_markup=markup
            )
        bot.register_next_step_handler(msg, sceltaMedia)

def esplora(message):
    markup=types.ReplyKeyboardRemove()
    if message.text == "Esplora" :
        cartelleText, cartelleList = DeviceNavigation.esplora()
        if len(cartelleList)==0:
            bot.send_message(
                message.chat.id,
                "Nessuna cartella presente.\nTorno indietro",
                reply_markup=markup
                )
            goBack(message)
        else :
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Torna","Annulla")
            for cartella in cartelleList:
                markup.add(cartella)
            msg = bot.send_message(
                message.chat.id,
                cartelleText,
                reply_markup=markup
                )
            bot.register_next_step_handler(msg, sceltaCartella)
    elif message.text == "Torna":
        torna(message)
    else:
        annulla(message)
        
def sceltaMedia(message):
    if message.text == "Esplora":
        esplora(message)
        return
    elif message.text == "Torna":
        torna(message)
        return
    elif message.text == "Annulla":
        annulla(message)
        return
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(telecomando())
    DeviceNavigation.sceltaMedia(DeviceNavigation.getMedia(), message.text)
    bot.send_message(
            message.chat.id,
            "Media impostato",
            reply_markup=markup
            )
    
def sceltaCartella (message):
    if message.text == "Torna":
        torna(message)
        return
    elif message.text == "Annulla":
        annulla(message)
        return
    os.chdir(os.path.join(os.getcwd(),message.text))
    inCartella(message)
    
def goBack(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    mediaText, mediaList = DeviceNavigation.displayMedia()
    if len(mediaList) == 0:
        markup.add("Torna","Annulla")
        msg = bot.send_message(
            message.chat.id,
            "Non ci sono media in questa cartella\nVuoi tornare alla cartella padre?",
            reply_markup=markup
            )
        bot.register_next_step_handler(msg, torna)
    else:
        markup.add("Esplora","Torna")
        for file in mediaList:
            markup.add(file)
        msg = bot.send_message(
            message.chat.id,
            mediaText + "\nScegli il file da riprodurre, oppure Esplora se vuoi esplorare il file system",
            reply_markup=markup
            )
        bot.register_next_step_handler(msg, sceltaMedia)

def torna(message):
    markup=types.ReplyKeyboardRemove()

    if DeviceNavigation.isMountpoint(os.getcwd()):
        cartelle = list(os.walk(os.getcwd()))[0][1]
        media = DeviceNavigation.getMedia()
        if len(cartelle)==0 and len(media)==0:
            DeviceNavigation.backHome()
            bot.send_message(
                message.chat.id,
                "In questo dispositivo non ci sono cartelle nè media.\nOperazione annullata",
                reply_markup=markup
                )
        else:
            bot.send_message(
                message.chat.id,
                "Radice raggiunta, non puoi tornare indietro.\nUsa /selezionaDispositivo se vuoi cambiare dispositivo",
                reply_markup=markup
                )
            inCartella(message)
        return

    if message.text == "Torna" :
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
        inCartella(message)
    else:
        annulla(message)
        
def annulla(message):
    markup=types.ReplyKeyboardRemove()
    DeviceNavigation.backHome()
    bot.send_message(
        message.chat.id,
        "Operazione annullata",
        reply_markup=markup
        )
    

    
#=============================================================================================================================================
#                                                   Comandi per VLC
#=============================================================================================================================================

def telecomando():
    telecomando = [] 

    if VLCHandler.getState() == State.Stopped:
        return ["Play"]

    primaRiga = ["-10"]
    if VLCHandler.getState() == State.Paused:
        primaRiga.append("Play")
    elif VLCHandler.getState() == State.Playing:
        primaRiga.append("Pause")
    primaRiga.append("+10")

    telecomando.append(primaRiga)

    secondaRiga=[]
    if VLCHandler.isMute():
        secondaRiga.append("Riattiva volume")
    else:
        secondaRiga.append("Muto")

    if VLCHandler.isFullScreen():
        secondaRiga.append("Finestra")
    else:
        secondaRiga.append("Schermo intero")

    telecomando.append(primaRiga)

    telecomando.append(["Stop"])
    
    return telecomando


@bot.message_handler(func=lambda message: isMediaMode() and message.text=="Play")
def play(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    if not isMediaModeHandler(message):
        return
    
    VLCHandler.play()

    markup.add(telecomando())
    
    bot.send_message(
        message.chat.id,
        "Inizio riproduzione",
        reply_markup=markup
        )
    
@bot.message_handler(func=lambda message: isMediaMode() and message.text=="Pause")
def pause(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    if not isMediaModeHandler(message):
        return

    VLCHandler.pause()
    
    markup.add(telecomando())
    
    bot.send_message(
        message.chat.id,
        "Media in pausa",
        reply_markup=markup
        )
    
@bot.message_handler(func=lambda message: isMediaMode() and message.text=="Stop")
def stop(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    if not isMediaModeHandler(message):
        return

    VLCHandler.stop()
    
    markup.add(telecomando())
    
    bot.send_message(
        message.chat.id,
        "Riproduzione interrotta",
        reply_markup=markup
        )
    
@bot.message_handler(func=lambda message: isMediaMode() and (message.text=="+10" or message.text=="-10"))
def skip(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    if not isMediaModeHandler(message):
        return

    VLCHandler.skip(message.text)
    
    markup.add(telecomando())
    
    bot.send_message(
        message.chat.id,
        "Skip " + message.text + " secondi",
        reply_markup=markup
        )
    
@bot.message_handler(func=lambda message: isMediaMode() and (message.text=="Finestra" or message.text=="Schermo intero"))
def pause(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    if not isMediaModeHandler(message):
        return

    VLCHandler.toggleFullScreen()
    
    markup.add(telecomando())
    
    bot.send_message(
        message.chat.id,
        "Schermo intero:" + str(VLCHandler.isFullScreen()),
        reply_markup=markup
        )
    
@bot.message_handler(func=lambda message: isMediaMode() and (message.text=="Muto" or message.text=="Riattiva volume"))
def pause(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    if not isMediaModeHandler(message):
        return

    VLCHandler.toggleFullScreen()
    
    markup.add(telecomando())
    
    bot.send_message(
        message.chat.id,
        "Muto:" + str(VLCHandler.isMute()),
        reply_markup=markup
        )



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