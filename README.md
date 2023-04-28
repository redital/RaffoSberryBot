# RaffoSberryBot
 Bot telegram per il controllo di un RaspberryPi.
 
 L'intento è di creare un bot che mi permetta una totale gestione del Raspberry. L'idea è di strutturarlo diviso in modalità, a seconda della tipologia di funzione che si vuole utilizzare. Inizialmente ci si trova in modalità "Hub" da cui è possibile spostarsi nelle varie altre modalità.
 Attualmente si è completato lo sviluppo della prima modalità: Media che permette di eseguire file multimediali da dispositivi di archiviazione esterna

Migliorie da fare:
- Aggiungere chiusura eventuali player ulteriori aperti in reset
- Refactoring

## Prossime idee: 
- Introdurre un'attività di scraping di canali telegram per scaricare media in automatico dai canali
- Introdurre una modalità di lettura dei log (incluso monitoraggio temperatura)
- Introdurre un tasto nell'hub per il reboot del raspberry
