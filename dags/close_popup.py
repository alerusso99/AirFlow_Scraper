from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# Questa funzione si occupa di chiudere il popup che si apre al primo accesso del sito.
def fun_close_popup(driver, wait):
    # Identifichiamo il frame contenente il popup che appare la prima volta che entriamo sul sito.
    frame_popup = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='automizely_marketing_popup_bars']")))

    # Passiamo il controllo al frame identificato(pop-up).
    driver.switch_to.frame(frame_popup)

    # Identifichiamo il bottone per la chiusura del popup.
    bottone_close_popup = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[1]/div/button")))

    # Clicchiamo il bottone così da chiudere il pop-up.
    bottone_close_popup.click()

    # Passiamo il controllo al frame principale(è quello di default).
    driver.switch_to.default_content()