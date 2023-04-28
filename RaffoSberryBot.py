import telebot
from telebot import types
from telebot import apihelper
import CoseSegrete
import DeviceNavigation
import VLCHandler
import os
from time import sleep
from datetime import timedelta, datetime
from vlc import State

API_TOKEN = CoseSegrete.TOKEN

apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot(API_TOKEN)

DeviceNavigation.init()

mode = "Hub"

lastActivity = datetime.now()

autenticato = False

inactivityTime = timedelta(hours = 1, seconds = 0)

#=============================================================================================================================================
#                                           Solo il proprietario del Raffosberry può usare questo bot!
#=============================================================================================================================================


@bot.message_handler(func=lambda message: message.chat.id!=CoseSegrete.owner_id)
def isOwnerHandler(message):
    bot.send_message(message.chat.id, "Solo il proprietario del Raffosberry può usare questo bot!")
    return

def reset(message):
    global mode
    if mode=="Media":
        DeviceNavigation.backHome()
        VLCHandler.stop()
        
    mode = "Hub"
    
    markup=types.ReplyKeyboardRemove()

    msg = bot.send_message(message.chat.id,"reset", reply_markup=markup)
    bot.delete_message(msg.chat.id,msg.id)

def isAuthenticated(message):
    now =  datetime.fromtimestamp(message.date)
    print(type(now))
    delta = now - lastActivity
    print(type(delta))
    print((delta))
    print(type(inactivityTime))
    print((inactivityTime))
    print()
    if delta > inactivityTime :
        global autenticato
        autenticato = False
        reset(message)
    return autenticato
    
def autenticazione(message):
    if message.text == CoseSegrete.Password:
        global autenticato
        autenticato = True
        global lastActivity
        lastActivity = datetime.fromtimestamp(message.date)
        bot.send_message(message.chat.id, "Benvenuto!")
        bot.delete_message(message.chat.id,message.id)
    else:
        bot.send_message(message.chat.id, "Password errata!")
        bot.delete_message(message.chat.id,message.id)
        isAuthenticatedHandler(message)

@bot.message_handler(func=lambda message: not isAuthenticated(message))
def isAuthenticatedHandler(message):
    markup=types.ReplyKeyboardRemove()
    msg = bot.send_message(message.chat.id, "Devi autenticarti!\nInserisci la tua password", reply_markup=markup)
    bot.register_next_step_handler(msg, autenticazione)

@bot.middleware_handler(update_types=['message'])
def updateLastActivity(bot_instance, message):
    if isAuthenticated(message):
        global lastActivity
        lastActivity = datetime.fromtimestamp(message.date)
        print("Aggiornato " + str(lastActivity))
        print()


#=============================================================================================================================================
#                                                   Operazioni generiche e preliminari
#=============================================================================================================================================


@bot.message_handler(commands=['start'])
def start(message):
    reset(message)
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
Adesso ti trovi nell'hub, digita (o premi) /media per entrare nella modalità media in cui portrai visualizzare i file multimediali presenti in una evenutale periferica collegata e riprodurne il contenuto

Purtroppo per ora c'è solo questa modalità, ma prima o poi ne aggiungerò altre!
    """
    messaggiHelp["Media"] = """\
Bot realizzato per il controllo del fantastico RaffoSberry.
Adesso ti trovi in modalità media in cui portrai visualizzare i media presenti in una evenutale periferica collegata e riprodurne il contenuto. 
Digita (o premi) /hub per tornare all'hub
Se invece vuoi usare questra modalità, ti spiego un po' come funziona.

Per rendere tutto più semplice questo bot ha pochi comandi ma si affida per lo più sulle tastiere, si consiglia quindi di usare quelle piuttosto che scrivere da se gli input.

Per cominciare puoi digitare (o premere) /selezionaDispositivo per scegliere da quale periferica si vuole leggere i file multimediali. I tasti che compariranno mostrano il nome della periferica o della partizione interessata, da questa però spesso non si capisce molto, si può quindi usare /dispositivi per avere qualche informazione in più (non dimenticare di usare di nuovo /selezionaDispositivo poi per scegliere!).
Una volta scelta la periferica si può navigare al suo interno. Leggi i messaggi che riceverai, usa le tastiere che compariranno e sarà facilissimo!

Scelto il file multimediale comparirà il telecomando, è una tastiera come tutte le altre ma è quella che ti permette effettivamente di comandare la riproduzione del file multimediale. 
I tasti del telecomando ti permetteranno di:
Tornare indietro di 10 secondi
Andare avati di 10 secondi
Fermare/riprendere la riproduzione (play/pausa)
Attivare/disattivare il muto
Attivare/disattivare il fullscreen
Sapere quanto manca al termine della riproduzione
Interrompere la riproduzione
In ogni momento anche durante la riproduzione si può riprendere la navigazione del file system ricominciando da /selezionaDispositivo, per ritrovare il telecomando basterà scrivere telecomando in qualsiasi momento.

Buona visione!
    """

    bot.send_message(message.chat.id, messaggiHelp[mode], reply_markup=markup)

@bot.message_handler(commands=['lista'])
def listaComandi(message):
    markup=types.ReplyKeyboardRemove()

    messaggiHelp = {}
    messaggiHelp["Hub"] = """\
Sei nell'hub, i comandi che puoi usare sono:
/media - Entra in modalità media
    """
    messaggiHelp["Media"] = """\
Sei in modalità media, i comandi che puoi usare sono:
/hub - Torna all'hub
/dispositivi - Mostra la lista dei dispositivi di archiviazione esterna collegati
/selezionaDispositivo - Permette di scegliere da quale periferica si vuole leggere i file multimediali
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
def selezionaDispositivi(message):
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
    
    if not isAuthenticated(message):
        isAuthenticatedHandler(message)
        return
    
    selection = -1
    devices = DeviceNavigation.getUsbDevices()[0]
    for i in range(len(devices)):
        if message.text == devices[i]["NAME"]:
            selection = i
            DeviceNavigation.deviceSelection(devices,selection)
            inCartella(message)
            return
    if message.text == "/dispositivi":
        dispositivi(message)
    
def inCartella(message):
    
    if not isAuthenticated(message):
        isAuthenticatedHandler(message)
        return
    
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
    
    if not isAuthenticated(message):
        isAuthenticatedHandler(message)
        return
    
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
    
    if not isAuthenticated(message):
        isAuthenticatedHandler(message)
        return
    
    if message.text == "Esplora":
        esplora(message)
        return
    elif message.text == "Torna":
        torna(message)
        return
    elif message.text == "Annulla":
        annulla(message)
        return
    DeviceNavigation.sceltaMedia(DeviceNavigation.getMedia(), message.text)
    bot.send_message(
            message.chat.id,
            "Media impostato",
            reply_markup=telecomando()
            )
    
def sceltaCartella (message):
    
    if not isAuthenticated(message):
        isAuthenticatedHandler(message)
        return
    
    if message.text == "telecomando" and isMediaMode():
        riprendiTelecomando(message)
        return
    elif message.text == "Torna":
        torna(message)
        return
    elif message.text == "Annulla":
        annulla(message)
        return
    try:
        os.chdir(os.path.join(os.getcwd(),message.text))
    except:
        bot.send_message(
            message.chat.id,
            "Qualcosa è andato storto, forse hai sbaliato a digitare il nome della cartella?",
            reply_markup=types.ReplyKeyboardRemove()
            )
    inCartella(message)
    
def goBack(message):
    
    if not isAuthenticated(message):
        isAuthenticatedHandler(message)
        return
    
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
    
    if not isAuthenticated(message):
        isAuthenticatedHandler(message)
        return
    
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
    
    if not isAuthenticated(message):
        isAuthenticatedHandler(message)
        return
    
    markup=types.ReplyKeyboardRemove()
    DeviceNavigation.backHome()
    if message.text == "telecomando" and isMediaMode():
        riprendiTelecomando(message)
        return
    bot.send_message(
        message.chat.id,
        "Operazione annullata",
        reply_markup=markup
        )
    

    
#=============================================================================================================================================
#                                                   Comandi per VLC
#=============================================================================================================================================

def telecomando():
    telecomando = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    if VLCHandler.getState() == State.Stopped or VLCHandler.getState() == State.NothingSpecial: # C'è anche il caso Ended e Opening

        return telecomando.add("Play").add("Cambia media")

    if VLCHandler.getState() == State.Paused or VLCHandler.getState() == State.NothingSpecial:
        telecomando.add("-10","Play","+10")
    elif VLCHandler.getState() == State.Playing:
        telecomando.add("-10","Pause","+10")

    elemento1 = ""
    if not VLCHandler.isMute():
        elemento1 = "Riattiva volume"
    else:
        elemento1 = "Muto"

    elemento2=""
    if not VLCHandler.isFullScreen():
        elemento2 = "Finestra"
    else:
        elemento2 = "Schermo intero"

    telecomando.add(elemento1,elemento2)

    telecomando.add("Quanto manca?")

    telecomando.add("Stop")
    
    return telecomando


@bot.message_handler(func=lambda message: isMediaMode() and message.text=="Play")
def play(message):

    if not isMediaModeHandler(message):
        return
    
    VLCHandler.play()
    
    sleep(2.0)
    
    bot.send_message(
        message.chat.id,
        "Inizio riproduzione",
        reply_markup=telecomando()
        )
    
@bot.message_handler(func=lambda message: isMediaMode() and message.text=="Pause")
def pause(message):

    if not isMediaModeHandler(message):
        return

    VLCHandler.pause()
    
    
    bot.send_message(
        message.chat.id,
        "Media in pausa",
        reply_markup=telecomando()
        )
    
@bot.message_handler(func=lambda message: isMediaMode() and message.text=="Stop")
def stop(message):

    if not isMediaModeHandler(message):
        return

    VLCHandler.stop()
    
    bot.send_message(
        message.chat.id,
        "Riproduzione interrotta",
        reply_markup=telecomando()
        )
    
@bot.message_handler(func=lambda message: isMediaMode() and ((message.text[0]=="+" and str(message.text[1:]).isnumeric()) or (message.text[0]=="-" and str(message.text[1:]).isnumeric())))
def skip(message):

    if not isMediaModeHandler(message):
        return

    VLCHandler.skip(int(message.text))
    
    bot.send_message(
        message.chat.id,
        "Skip " + message.text + " secondi",
        reply_markup=telecomando()
        )
    
@bot.message_handler(func=lambda message: isMediaMode() and (message.text=="Finestra" or message.text=="Schermo intero"))
def pause(message):

    if not isMediaModeHandler(message):
        return

    VLCHandler.toggleFullScreen()
    
    sleep(0.5)
    
    bot.send_message(
        message.chat.id,
        "Schermo intero:" + str(not VLCHandler.isFullScreen()),
        reply_markup=telecomando()
        )
    
@bot.message_handler(func=lambda message: isMediaMode() and (message.text=="Muto" or message.text=="Riattiva volume"))
def pause(message):

    if not isMediaModeHandler(message):
        return

    VLCHandler.toggleMute()
    
    sleep(0.5)

    bot.send_message(
        message.chat.id,
        "Muto:" + str(not VLCHandler.isMute()),
        reply_markup=telecomando()
        )
    
@bot.message_handler(func=lambda message: isMediaMode() and message.text=="Quanto manca?")
def stop(message):

    if not isMediaModeHandler(message):
        return

    bot.send_message(
        message.chat.id,
        VLCHandler.quantoManca(),
        reply_markup=telecomando()
        )
    
@bot.message_handler(func=lambda message: isMediaMode() and str(message.text).lower()=="telecomando")
def riprendiTelecomando(message):

    if VLCHandler.vlcplayer.get_media()==None:
        bot.send_message(
        message.chat.id,
        "Imposta prima un media!",
        reply_markup=types.ReplyKeyboardRemove()
        )
        selezionaDispositivi(message)
        return
    
    if not isMediaModeHandler(message):
        return

    bot.send_message(
        message.chat.id,
        "Hai perso il telecomando? Eccolo qua!",
        reply_markup=telecomando()
        )
    
@bot.message_handler(func=lambda message: isMediaMode() and message.text=="Cambia media")
def cambiaMedia(message):

    if not isMediaModeHandler(message):
        return

    inCartella(message)






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