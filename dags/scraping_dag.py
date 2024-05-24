from airflow.decorators import dag, task
from datetime import datetime, timedelta
import final_functions

default_args = {
    'owner': 'alessandro',
    'retries': 5,
    'retry_delay': timedelta(minutes=10),
}

@dag(dag_id='airflow_scraping',
    default_args=default_args,
    description='Effettuiamo lo scraping del sito web tramontano.it, aggiorniamo il db postgres e inviamo i nuovi '
                'prodotti ad un server.',
    start_date=datetime(2024, 5, 20),
    schedule_interval='@weekly')
def esecuzione():

    @task()
    def scraping():
        lista_prodotti = final_functions.scraping_web()
        return lista_prodotti

    @task()
    def aggiorna_db(lista_prodotti):
        lista_nuovi = final_functions.aggiorna_database(lista_prodotti)
        return lista_nuovi

    @task()
    def aggiorna_server(lista_nuovi):
        final_functions.aggiorna_server(lista_nuovi)


    lista_prodotti = scraping()
    lista_nuovi = aggiorna_db(lista_prodotti)
    aggiorna_server(lista_nuovi)

dag = esecuzione()