from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# Questa funzione ci ritornerà una lista, contenente i link di tutti i prodotti di una pagina del catalogo.
def find_catalog_products(wait):
    # Identifichiamo tutti i prodotti del catalogo.
    catalog_elements = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "Grid__Cell")))
    # Creiamo una lista per salvare i link dei prodotti.
    lista_link = []
    # Iteriamo sugli elementi del catalogo e otteniamo i loro riferimenti.
    for elemento in catalog_elements:
        # Prendiamo il riferimento ad un elemento specifico del catalogo.
        link_elemento = elemento.find_element(By.TAG_NAME, 'a')
        # Ricaviamone il link.
        link = link_elemento.get_attribute('href')
        # Aggiungiamo il link alla lista.
        lista_link.append(link)
    return lista_link