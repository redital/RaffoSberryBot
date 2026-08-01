import alsaaudio
from logger import get_logger

logger = get_logger(__name__)

def _get_mixer():
    """Funzione interna di utilità per agganciare il canale Master."""
    try:
        return alsaaudio.Mixer('Master')
    except alsaaudio.ALSAAudioError:
        # Se il canale 'Master' non esiste, prova a usare il primo disponibile
        mixers = alsaaudio.mixers()
        if mixers:
            logger.warning("Mixer 'Master' non trovato, uso '%s' al suo posto", mixers[0])
            return alsaaudio.Mixer(mixers[0])
        logger.error("Nessun mixer ALSA trovato sul sistema")
        raise RuntimeError("Nessun mixer ALSA trovato sul sistema.")

def get_volume():
    """Ritorna il volume attuale (0-100) del canale sinistro (Mono/Stereo compatibile)."""
    try:
        mixer = _get_mixer()
        # getvolume() restituisce una lista (es. [65, 65] per Left/Right)
        volume = mixer.getvolume()[0]
        logger.debug("Volume letto: %s", volume)
        return volume
    except Exception:
        logger.exception("Errore durante la lettura del volume, ritorno 0")
        return 0

def set_volume(percentuale):
    """Imposta il volume a una percentuale specifica (0-100)."""
    # Protezione per rimanere nel range corretto
    percentuale_clampata = max(0, min(100, percentuale))
    if percentuale_clampata != percentuale:
        logger.warning(
            "Volume richiesto %s fuori range, corretto a %s",
            percentuale, percentuale_clampata
        )
    try:
        mixer = _get_mixer()
        mixer.setvolume(percentuale_clampata)
        logger.info("Volume impostato a %s", percentuale_clampata)
        return percentuale_clampata
    except Exception:
        logger.exception("Errore durante l'impostazione del volume a %s", percentuale_clampata)
        return 0

def modifica_volume(delta):
    """Alza o abbassa il volume di un valore fisso (es: +10 o -10)."""
    vol_attuale = get_volume()
    nuovo_vol = vol_attuale + delta
    logger.debug("Modifica volume: %s -> %s (delta %s)", vol_attuale, nuovo_vol, delta)
    return set_volume(nuovo_vol)