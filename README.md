# AirFlow_Scraper_Web_Selenium

Il progetto riguarda uno script Python progettato per effettuare il web scraping su un sito web di borse, estraendo informazioni sui prodotti e popolando un database relazionale con i dati raccolti. I nuovi prodotti identificati vengono inviati tramite un messaggio JSON a un server esterno per l'aggiornamento dei suoi database relazionale e vettoriale. Lo script parte in automatico, una volta a settimana, tramite il software di orchestrazione Airflow.

## Funzionalità

- **Web Scraping**: Utilizza Selenium per navigare e estrarre informazioni dettagliate sulle borse da un sito web.
- **Popolamento Database**: Inserisce i dati estratti in un database relazionale.
- **Notifica dei Nuovi Prodotti**: Invia un messaggio JSON a un server esterno per aggiornare i database con i nuovi prodotti.

## Tecnologie Utilizzate

- Python 3.10
- Selenium
- Un driver per il browser (es. ChromeDriver per Google Chrome)
- Un database relazionale PostgreSQL
- Una connessione al server che riceverà i messaggi JSON
- Airflow

## Prerequisiti per mandarlo in esecuzione
- docker
- docker-compose
- WebDriver Chrome
