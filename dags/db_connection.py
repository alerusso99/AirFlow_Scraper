from dotenv import load_dotenv
import psycopg2


# Questa funzione ha l'obiettivo di stabilire una connessione con il db.
def connect_to_db():
    # Carichiamo le credenziali.
    load_dotenv()
    # Indichiamo il nome del db.
    dbname = "airflow"
    # Indichiamo lo username dell'admin del db.
    user = "airflow"
    # Indichiamo la password dell'admin del db.
    password = "airflow"
    # Indichiamo l'host del db.
    host = 'postgres'
    # Indichiamo la porta su cui il db è in ascolto.
    port = '5432'
    try:
        # Effettuiamo la connessione al db.
        conn = psycopg2.connect(dbname=dbname, host=host, user=user, password=password, port=port)
        print("Connessione al database riuscita!")
    except psycopg2.Error as e:
        print("Errore durante la connessione al database:", e)
    return conn


# Apriamo il cursore che ci consentirà di interagire con il db.
def open_cursor(conn):
    cur = conn.cursor()
    return cur


# Questa funzione ci permette di chiudere il cursore quando abbiamo completato le nostre operazioni.
def close_cursor(cur):
    cur.close()


# Questa funzione ci permette di chiudere la connessione con il db.
def close_connection(conn):
    conn.close()


# Questa funzione verifica se, un prodotto trovato facendo lo scraping del sito, era già presente nel db o se bisogna
# aggiungerlo.
def query_search_db(cur, conn, lista_prodotti):
    lista_nuovi = []
    for prodotto in lista_prodotti:
        query = "SELECT * FROM borsa WHERE product_url = %s"
        cur.execute(query, (prodotto.url_product,))
        # Nel caso in cui il prodotto non sia presente nel db, lo aggiungiamo.
        if cur.rowcount == 0:
            lista_nuovi.append(prodotto)
            query_insert_db(cur, conn, prodotto)
    return lista_nuovi


# Questa funzione si occupa di inserire un nuovo prodotto nel db.
def query_insert_db(cur, conn, prodotto):
    query = "INSERT INTO borsa (nome, prezzo, descrizione, materiale, colore, dimensione, img_url, product_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(query, (prodotto.nome, prodotto.prezzo, prodotto.descrizione, prodotto.materiale, prodotto.colore, prodotto.dimensione, prodotto.url_immagine, prodotto.url_product))
    conn.commit()

