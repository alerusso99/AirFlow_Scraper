import json
import requests


# Questa funzione ci permette di inviare un messaggio al server contenente tutti i nuovi prodotti da aggiungere al
# suo db.
def aggiorna_server(lista_prodotti_nuovi):
    url = "http://52.9.244.32:8000/controller/update_db"
    # Creiamo un messaggio json contenente tutti i prodotti da inviare al server.
    json_lista_prodotti_nuovi = json.dumps([p.to_dict() for p in lista_prodotti_nuovi])
    headers = {
        'Content-Type': 'application/json'
    }
    # Stampiamo a schermo il messaggio json creato.
    print(json_lista_prodotti_nuovi)
    # Inviamo la richiesta al server.
    response = requests.post(url, data=json_lista_prodotti_nuovi, headers=headers)
    # Controlla la risposta del server
    if response.status_code == 200:
        print("Messaggio inviato con successo al server.")
    else:
        print("Si è verificato un errore durante l'invio del messaggio.")
