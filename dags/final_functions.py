import close_popup
import definition_browser
import catalog_products
import catalog_page
import product_information
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
import db_connection
import connection_server


def scraping_web():
    while True:
        try:
            # Creiamo un istanza del browser che vogliamo utilizzare.
            driver = definition_browser.fun_definition_browser()

            # Ci rechiamo alla seguente pagina.
            driver.get("https://tramontano.it/collections/nuovi-arrivi")

            # Impostiamo il tempo di attesa massimo a 120 secondi.
            wait = WebDriverWait(driver, 120)

            # Chiamiamo questa funzione per chiudere il popup che si apre al primo accesso del sito.
            close_popup.fun_close_popup(driver, wait)

            # Ricaviamo il numero di pagine del catalogo.
            numero_pagine = catalog_page.find_max_page(wait)

            # Definiamo una lista che conterrà i prodotti del catalogo per ogni pagina.
            lista_prodotti = []

            # Per ogni pagina del catalogo.
            for i in range(1, int(numero_pagine)+1):
                # Quando siamo in una pagina del catalogo, la prima operazione da fare è uno scroll di 500px in verticale,
                # così da far caricare eventuali elementi del catalogo.
                driver.execute_script("window.scrollBy(0, 500);")
                # Attendiamo 10 secondi, il caricamento degli elementi della pagina che ci servono.
                time.sleep(10)
                # Ci ricaviamo i link di tutti i prodotti presenti nella pagina corrente del catalogo.
                lista_prodotti_link = catalog_products.find_catalog_products(wait)
                # Per ogni link che abbiamo recuperato.
                for link in lista_prodotti_link:
                    # Ci rechiamo al seguente link.
                    driver.get(link)
                    # Salviamo in una variabile url_product il link del prodotto.
                    url_product = product_information.retrieve_url_product(link)
                    # Ricaviamo il nome del prodotto.
                    nome = product_information.retrieve_name(wait)
                    # Ricaviamo il prezzo del prodotto.
                    prezzo = product_information.retrieve_price(wait)
                    # Ricaviamo la descrizione generale del prodotto.
                    descrizione_generale = product_information.retrieve_description_general(wait)
                    # Estrapoliamo la descrizione vera e propria del prodotto.
                    descrizione = product_information.retrieve_description(descrizione_generale)
                    # Estrapoliamo il colore del prodotto.
                    colore = product_information.retrieve_color(descrizione_generale)
                    # Estrapoliamo il materiale del prodotto.
                    materiale = product_information.retrieve_material(descrizione_generale)
                    # Estrapoliamo la dimensione del prodotto.
                    dimensione = product_information.retrieve_dimension(descrizione_generale)
                    # Ricaviamo l'url dell'immagine del prodotto.
                    img_url = product_information.retrieve_img_url(wait)
                    prodotto = product_information.Prodotto(
                        url_product, nome, prezzo, descrizione, materiale, colore, dimensione, img_url)
                    lista_prodotti.append(prodotto.to_dict())
                # Ripuliamo la lista caricata precedentemente.
                lista_prodotti_link.clear()
                # Creiamo il link per passare alla pagina successiva del catalogo.
                next_page_link = catalog_page.create_link(i + 1)
                # Ci rechiamo alla pagina successiva del catalogo.
                driver.get(next_page_link)
            break
        except TimeoutException:
            # In caso di TimeoutException, chiudiamo il browser, puliamo le liste e ricominciamo tutto da capo.
            driver.quit()
            lista_prodotti.clear()
            lista_prodotti_link.clear()

    # Chiude il browser
    driver.quit()
    return lista_prodotti


def aggiorna_database(lista_prodotti):
    # Riconverti i dizionari in oggetti Prodotto
    lista_prodotti_obj = [product_information.dict_to_prodotto(prod) for prod in lista_prodotti]
    lista_nuovi_json = []
    # Ci colleghiamo al db.
    connection = db_connection.connect_to_db()
    # Apriamo un cursore.
    cursor = db_connection.open_cursor(connection)
    # Iniziamo la ricerca nel db, per individuare eventuali nuovi prodotti.
    lista_nuovi = db_connection.query_search_db(cursor, connection, lista_prodotti_obj)
    for prodotto in lista_nuovi:
        lista_nuovi_json.append(prodotto.to_dict())
    # Chiudiamo il cursore.
    db_connection.close_cursor(cursor)
    # Chiudiamo la connessione.
    db_connection.close_connection(connection)
    return lista_nuovi_json


def aggiorna_server(lista_nuovi):
    lista_nuovi_obj = [product_information.dict_to_prodotto(prod) for prod in lista_nuovi]
    # Se la lista non è vuota:
    if lista_nuovi_obj:
        # Aggiorniamo il server con la lista dei nuovi prodotti.
        connection_server.aggiorna_server(lista_nuovi_obj)
