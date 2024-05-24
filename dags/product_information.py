from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# Definiamo una classe Prodotto
class Prodotto:
    def __init__(self, url_product, nome, prezzo, descrizione, materiale, colore, dimensione, url_immagine):
        self.url_product = url_product
        self.nome = nome
        self.prezzo = prezzo
        self.descrizione = descrizione
        self.materiale = materiale
        self.colore = colore
        self.dimensione = dimensione
        self.url_immagine = url_immagine

    def __str__(self):
        return f"{self.nome} - {self.prezzo} €\nDescrizione: {self.descrizione}\nMateriale: {self.materiale}\nColore: {self.colore}\nDimensione: {self.dimensione}\nURL Immagine: {self.url_immagine}\nURL Prodotto: {self.url_product}"

    def to_dict(self):
        return {
            'url_product': self.url_product,
            'nome': self.nome,
            'prezzo': self.prezzo,
            'descrizione': self.descrizione,
            'materiale': self.materiale,
            'colore': self.colore,
            'dimensione': self.dimensione,
            'url_immagine': self.url_immagine
        }


# Questa funzione ci ritorna l'url del prodotto.
def retrieve_url_product(link):
    urlProdottoVariable = link
    return urlProdottoVariable


# Questa funzione converte un json in un oggetto.
def dict_to_prodotto(d):
    return Prodotto(
        d['url_product'], d['nome'], d['prezzo'], d['descrizione'],
        d['materiale'], d['colore'], d['dimensione'], d['url_immagine']
    )


# Questa funzione ci serve a ricavare il nome del prodotto.
def retrieve_name(wait):
    # Identifichiamo l'elemento contenente il nome del prodotto.
    nomeBorsa = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.ProductMeta__Title')))
    # Otteniamo del testo dalla variabile nomeBorsa.
    nomeBorsaVariable = nomeBorsa.text
    # Rimuoviamo dalla stringa l'eventuale presenza di ZWNBSP
    nomeBorsaVariable = nomeBorsaVariable.replace("\uFEFF", "")
    return nomeBorsaVariable


# Questa funzione ci serve a ricavare il prezzo del prodotto.
def retrieve_price(wait):
    # Identifichiamo l'elemento contenente il prezzo della borsa.
    prezzoBorsa = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.ProductMeta__Price')))
    # Otteniamo del testo dalla variabile prezzoBorsa.
    prezzoBorsaVariable = prezzoBorsa.text
    # Rimuoviamo dalla stringa l'eventuale presenza di ZWNBSP
    prezzoBorsaVariable = prezzoBorsaVariable.replace("\uFEFF", "")
    return prezzoBorsaVariable


# Questa funzione ci serve a ricavare la descrizione generale del prodotto.
def retrieve_description_general(wait):
    # Identifichiamo l'elemento contenente la descrizione generale della borsa.
    descrizioneBorsa = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.ProductMeta__Description')))
    # Otteniamo del testo dalla variabile descrizioneBorsa
    descrizioneBorsaVariable = descrizioneBorsa.text
    # Rimuoviamo dalla stringa l'eventuale presenza di ZWNBSP
    descrizioneBorsaVariable = descrizioneBorsaVariable.replace("\uFEFF", "")
    return descrizioneBorsaVariable


# Questa funzione ci serve a ricavare l'url dell'immagine del prodotto.
def retrieve_img_url(wait):
    # Identifichiamo l'elemento contenente l'immagine del prodotto.
    imgBorsa = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.Image--lazyLoaded')))
    # Ricaviamo l'URL dell'immaggine.
    image_url = imgBorsa.get_attribute('data-original-src')
    # Aggiungiamo il protocollo https all'URL
    if image_url.startswith('//'):
        image_url = 'https:' + image_url
    return image_url


# Questa funzione ci permette di ricavare la descrizione vera e propria del prodotto. Verranno fatte tante operazioni
# per estrapolare dalla variabile descrizione generale, soltanto la descrizione vera e propria del prodotto.
def retrieve_description(description_general):
    materiale_stringa = "MATERIALE:"
    materiali_stringa = "MATERIALI:"
    indice_materiale = description_general.find(materiale_stringa)
    indice_materiali = description_general.find(materiali_stringa)
    if indice_materiale != -1:
        descrizione = description_general[:indice_materiale]
        descrizione = descrizione.replace("Descrizione: ", "")
        descrizione = descrizione.replace("\n", "")
        descrizione = descrizione.replace("  ", " ")
    elif indice_materiali != -1:
        descrizione = description_general[:indice_materiali]
        descrizione = descrizione.replace("Descrizione: ", "")
        descrizione = descrizione.replace("\n", "")
    return descrizione


# Questa funzione ci permette di ricavare il materiale del prodotto. Verranno fatte tante operazioni per estrapolare
# dalla variabile descrizione generale, soltanto il materiale del prodotto.
def retrieve_material(description_general):
    materiale_stringa = "MATERIALE:"
    colori_stringa = "COLORI:"
    materiali_stringa = "MATERIALI:"
    colore_stringa = "COLORE:"
    indice_materiale = description_general.find(materiale_stringa)
    indice_colori = description_general.find(colori_stringa)
    indice_materiali = description_general.find(materiali_stringa)
    indice_colore = description_general.find(colore_stringa)
    if indice_materiale != -1 and indice_colore != -1:
        materiale = description_general[indice_materiale + len(materiale_stringa):indice_colore].strip()
        materiale = materiale.replace("\n", "")
    elif indice_materiale != -1 and indice_colori != -1:
        materiale = description_general[indice_materiale + len(materiale_stringa):indice_colori].strip()
        materiale = materiale.replace("\n", "")
    elif indice_materiali != -1 and indice_colore != -1:
        materiale = description_general[indice_materiali + len(materiali_stringa):indice_colore].strip()
        materiale = materiale.replace("\n", "")
    elif indice_materiali != -1 and indice_colori != -1:
        materiale = description_general[indice_materiali + len(materiali_stringa):indice_colori].strip()
        materiale = materiale.replace("\n", "")
    return materiale


# Questa funzione ci permette di ricavare il colore del prodotto.
# Verranno fatte tante operazioni per estrapolare dalla variabile descrizione generale, soltanto il colore del prodotto.
def retrieve_color(description_general):
    colore_stringa = "COLORE:"
    dimensione_stringa = "DIMENSIONE:"
    colori_stringa = "COLORI:"
    dimensioni_stringa = "DIMENSIONI:"
    indice_colore = description_general.find(colore_stringa)
    indice_dimensione = description_general.find(dimensione_stringa)
    indice_colori = description_general.find(colori_stringa)
    indice_dimensioni = description_general.find(dimensioni_stringa)
    if indice_colore != -1 and indice_dimensione != -1:
        colore = description_general[indice_colore + len(colore_stringa):indice_dimensione].strip()
        colore = colore.replace("\n", "")
    elif indice_colore != -1 and indice_dimensioni != -1:
        colore = description_general[indice_colore + len(colore_stringa):indice_dimensioni].strip()
        colore = colore.replace("\n", "")
    elif indice_colori != -1 and indice_dimensione != -1:
        colore = description_general[indice_colori + len(colori_stringa):indice_dimensione].strip()
        colore = colore.replace("\n", "")
    elif indice_colori != -1 and indice_dimensioni != -1:
        colore = description_general[indice_colori + len(colori_stringa):indice_dimensioni].strip()
        colore = colore.replace("\n", "")
    return colore


# Questa funzione ci permette di ricavare la dimensione del prodotto. Verranno fatte tante operazioni per estrapolare
# dalla variabile descrizione generale, soltanto la dimensione del prodotto.
def retrieve_dimension(description_general):
    dimensione_stringa = "DIMENSIONE:"
    dimensioni_stringa = "DIMENSIONI:"
    indice_dimensione = description_general.find(dimensione_stringa)
    indice_dimensioni = description_general.find(dimensioni_stringa)
    if indice_dimensione != -1:
        dimensione = description_general[indice_dimensione + len(dimensione_stringa):].strip()
        dimensione = dimensione.replace("\n", "")
    elif indice_dimensioni != -1:
        dimensione = description_general[indice_dimensioni + len(dimensioni_stringa):].strip()
        dimensione = dimensione.replace("\n", "")
    return dimensione

