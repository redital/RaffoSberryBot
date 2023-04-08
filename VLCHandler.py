import vlc

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

def mute():
    vlcplayer.audio_set_mute(True)

def unmute():
    vlcplayer.audio_set_mute(False)

def toggleMute():
    if vlcplayer.audio_get_mute():
        unmute()
    else:
        mute()

def fullScreen():
    vlcplayer.media_player.set_fullscreen(True)
