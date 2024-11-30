# RaffoSberryBot
 Bot telegram per il controllo di un RaspberryPi.
 
 L'intento è di creare un bot che mi permetta una totale gestione del RaspberryPi. L'idea è di strutturarlo diviso in modalità, a seconda della tipologia di funzione che si vuole utilizzare. Inizialmente ci si trova in modalità "Hub" da cui è possibile spostarsi nelle varie altre modalità.
 Attualmente si è completato lo sviluppo della prima modalità: Media che permette di eseguire file multimediali da dispositivi di archiviazione esterna

Migliorie da fare:
- Aggiungere chiusura eventuali player ulteriori aperti in reset
- Refactoring

## Prossime idee: 
- Introdurre un'attività di scraping di canali telegram per scaricare media in automatico dai canali
- Introdurre una modalità di lettura dei log (incluso monitoraggio temperatura)
- Introdurre un tasto nell'hub per il reboot del Raspberry
- Sto valutando di riavviare automaticamente il Raspberry quando non risponde per 10 secondi

N.B. il file di requirements è stato creato usando il comando pipreqs --ignore bin,etc,include,lib,lib64,.venv
Installare i requirements usando pip install -r requirements.txt
