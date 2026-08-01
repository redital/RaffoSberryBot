import vlc
from time import sleep
import os
import config
from logger import get_logger

logger = get_logger(__name__)

vlc_obj = None
vlcplayer = None

def setUp():
    global vlc_obj
    # Racchiudiamo tutti gli argomenti in una lista []
    vlc_obj = vlc.Instance([
        '--no-xlib', 
        '--verbose={}'.format(config.vlc_verbose), 
        '--avcodec-hw=none',
        '--file-caching=2000',
        '--live-caching=2000',
    ])   
    global vlcplayer
    vlcplayer = vlc_obj.media_player_new()

def clear():
    global vlc_obj
    vlc_obj = None
    global vlcplayer
    vlcplayer = None
    logger.info("VLC inizializzato (verbose=%s)", config.vlc_verbose)

def setMedia(src):
    logger.info("Imposto il media: %s", src)
    vlcmedia = vlc_obj.media_new(src) 
    vlcplayer.set_media(vlcmedia)

def play():
    logger.info("Play")
    vlcplayer.play()
def pause():
    logger.info("Pause")
    vlcplayer.pause()
def stop():
    logger.info("Stop")
    vlcplayer.stop()

def mute():
    logger.debug("Muto attivato")
    vlcplayer.audio_set_mute(True)

def unmute():
    logger.debug("Muto disattivato")
    vlcplayer.audio_set_mute(False)

def toggleMute():
    vlcplayer.audio_toggle_mute()
    logger.debug("Muto commutato (ora muto=%s)", not isMute())

def isMute():
    mute = vlcplayer.audio_get_mute()
    return not bool(mute)

def fullScreen():
    logger.debug("Fullscreen attivato")
    vlcplayer.set_fullscreen(True)

def toggleFullScreen():
    vlcplayer.toggle_fullscreen()
    logger.debug("Fullscreen commutato (ora fullscreen=%s)", not isFullScreen())

def isFullScreen():
    fullscreen = vlcplayer.get_fullscreen()
    return not bool(fullscreen)

def skip(n):
    logger.info("Skip di %s secondi", n)
    vlcplayer.set_time(vlcplayer.get_time()+(n*1000))

def autoclose():
    logger.debug("Attendo la fine della riproduzione per la chiusura automatica")
    while vlcplayer.is_playing():
        sleep(0.5)
    vlcplayer.stop()
    logger.info("Riproduzione terminata, chiusura automatica")

def quantoManca():
    posizione = vlcplayer.get_position()
    durata = vlcplayer.get_length()
    visto = vlcplayer.get_time()

    mancante = (durata-visto)//1000
    minuti = mancante//60
    secondi = mancante - (minuti*60)
    text = "Mancano {0} minuti e {1} secondi di media\nTrascorso: {2}%".format(minuti,secondi,(posizione*1000//1)/10)
    return text

def getState():
    return vlcplayer.get_state()
