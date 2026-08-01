import alsaaudio

def _get_mixer():
    """Funzione interna di utilità per agganciare il canale Master."""
    try:
        return alsaaudio.Mixer('Master')
    except alsaaudio.ALSAAudioError:
        # Se il canale 'Master' non esiste, prova a usare il primo disponibile
        mixers = alsaaudio.mixers()
        if mixers:
            return alsaaudio.Mixer(mixers[0])
        raise RuntimeError("Nessun mixer ALSA trovato sul sistema.")

def get_volume():
    """Ritorna il volume attuale (0-100) del canale sinistro (Mono/Stereo compatibile)."""
    try:
        mixer = _get_mixer()
        # getvolume() restituisce una lista (es. [65, 65] per Left/Right)
        return mixer.getvolume()[0]
    except Exception:
        return 0

def set_volume(percentuale):
    """Imposta il volume a una percentuale specifica (0-100)."""
    # Protezione per rimanere nel range corretto
    percentuale = max(0, min(100, percentuale))
    try:
        mixer = _get_mixer()
        mixer.setvolume(percentuale)
        return percentuale
    except Exception:
        return 0

def modifica_volume(delta):
    """Alza o abbassa il volume di un valore fisso (es: +10 o -10)."""
    vol_attuale = get_volume()
    nuovo_vol = vol_attuale + delta
    return set_volume(nuovo_vol)
