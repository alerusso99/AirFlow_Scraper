from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# Questa funzione serve a ricavare il numero massimo di pagine del catalogo.
def find_max_page(wait):
    # Identifichiamo gli elementi che compongono i numeri per passare da una pagina del catalogo ad un altra.
    numeri_pagina = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "Pagination__NavItem")))
    # Definiamo una lista, che conterrà gli elementi che abbiamo precedentemente identificato.
    lista_link_pagina = []
    # Aggiungiamo tutti gli elementi che abbiamo trovato alla lista.
    for numero in numeri_pagina:
        link_pagina = numero.get_attribute('text')
        lista_link_pagina.append(link_pagina)
    # Assegnamo alla variabile numero, l'elemento della lista che si trova nella penultima posizione.(L'ultima è
    # occupata dalla freccia per passare alla pagina successiva).
    numero = lista_link_pagina[len(lista_link_pagina)-2]
    return numero


# Funzione che serve a creare un link per passare ad una nuova pagina del catalogo, aggiungendo nella parte finale
# del link un indice che passeremo come parametro.
def create_link(indice):
    base_url = "https://tramontano.it/collections/nuovi-arrivi?page="
    link = base_url + str(indice)
    return link