import vlc
from time import sleep

vlc_obj = None
vlcplayer = None

def setUp():
    global vlc_obj
    vlc_obj= vlc.Instance()
    global vlcplayer
    vlcplayer = vlc_obj.media_player_new()

def setMedia(src):
    vlcmedia = vlc_obj.media_new(src) 
    vlcplayer.set_media(vlcmedia)

def play():
    vlcplayer.play()
def pause():
    vlcplayer.pause()
def stop():
    vlcplayer.stop()

def mute():
    vlcplayer.audio_set_mute(True)

def unmute():
    vlcplayer.audio_set_mute(False)

def toggleMute():
    vlcplayer.audio_toggle_mute()

def fullScreen():
    vlcplayer.set_fullscreen(True)

def fullScreen():
    vlcplayer.toggle_fullscreen()

def skip(n):
    vlcplayer.set_time(vlcplayer.get_time()+(n*1000))

def autoclose():
    while vlcplayer.is_playing():
        sleep(0.5)
    vlcplayer.stop()

def quantoManca():
    posizione = vlcplayer.get_position()
    durata = vlcplayer.get_length()
    visto = vlcplayer.get_time()

    mancante = (durata-visto)//1000
    minuti = mancante//60
    secondi = mancante - (minuti*60)
    text = "Mancano {0} minuti e {1} secondi di media\nTrascorso: {2}%".format(minuti,secondi,posizione*100//1)
