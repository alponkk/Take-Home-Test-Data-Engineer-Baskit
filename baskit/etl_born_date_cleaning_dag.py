from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
import gspread
import pandas as pd
import sqlite3


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'etl_born_date_cleaning',
    default_args=default_args,
    description='ETL process to clean and store born_date_data from csv to sqlite3',
    schedule_interval='@daily',
    start_date=days_ago(1),
    tags=['spreadsheet','cleaning','sqlite', 'etl'],
)


def etl(**kwargs):
    print("--- EXTRACT START ---")

    client = gspread.service_account('/opt/airflow/docker/database-385606-4a08c85dcd54.json')

    data = client.open("Salinan dari Take Home Test Data Engineer Baskit").worksheet("data").get_all_values()
    df = pd.DataFrame(data[2:], columns=data[1])

    print("--- EXTRACT SUCCESS ---")


    print("--- TRANSFORM START ---")
    # clean phone_number
    df['phone_number'] = df['phone_number'].str.replace(r'\D', '', regex=True)
    df['phone_number'] = df['phone_number'].apply(lambda x: '62' + x if x.startswith('8') else x if x.startswith('62') else None)

    # clean born_day
    def clean_born_day(born_day):
        try:
            return pd.to_datetime(born_day, errors='coerce').strftime('%Y-%m-%d')
        except ValueError:
            return None

    df['born_day'] = df['born_day'].apply(clean_born_day)

    print("--- TRANSFORM SUCCESS ---")


    print("--- LOAD SUCCESS ---")

    conn = sqlite3.connect('/opt/airflow/docker/db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS born_date_data (
            id TEXT PRIMARY KEY,
            name TEXT,
            phone_number TEXT,
            born_day DATE
        )
    ''')

    df.to_sql('born_date_data', conn, if_exists='replace', index=False)

    result = pd.read_sql_query("SELECT * FROM born_date_data LIMIT 10", conn)
    print("--- LOAD SUCCESS ---")

    
start = DummyOperator(
    task_id='start_etl',
    dag=dag
)

etl = PythonOperator(
    python_callable=etl,
    task_id='etl_born_date_cleaning',
    dag=dag
)

end = DummyOperator(
    task_id='finish_etl',
    dag=dag
)

start >> etl >> end