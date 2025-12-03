# Immagine base
FROM python:3.11

# Installazione di VLC e altre dipendenze (se non già incluse nel tuo codice)
RUN apt-get update && \
    apt-get install -y vlc x11-apps && \
    rm -rf /var/lib/apt/lists/*

# Impostazioni di lavoro
WORKDIR /app

# Copia i file necessari
COPY . /app

# Aggiorna pip
RUN pip install --upgrade pip

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Avvia l'app
CMD ["python", "RaffoSberryBot.py"]
