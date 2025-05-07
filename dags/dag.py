from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from sqlalchemy import create_engine
from datetime import datetime, timedelta


from elt import spotify_etl
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path="/opt/airflow/dags/.env")


def elt_run():
    print("started")
    df = spotify_etl()
    
    if df.empty:
        print("DataFrame is empty, skipping DB insert.")
        return

    conn = BaseHook.get_connection('postgres_spotify')
    uri = f"postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"
    engine = create_engine(uri)

    try:
        print(f"Inserting {len(df)} records into DB...")
        df.to_sql('spotify_tracks', engine, if_exists='append', index=False)
        print("✅ Insertion successful.")
    except Exception as e:
        print(f"❌ Insertion failed: {e}")



with DAG(dag_id='spotify_etl_dag',
        schedule_interval='*/5 * * * *',
        start_date=datetime(2025, 5, 3),
        catchup=False,
        default_args={
            'owner': 'airflow',
            'retries': 1,
            'retry_delay': timedelta(minutes=5),
            
        }
    ) as dag:
    create_Spotify_Tracks_table = PostgresOperator(
        task_id='create_spotify_tracks_table',
        postgres_conn_id='postgres_spotify',
        sql="""
            CREATE TABLE IF NOT EXISTS spotify_tracks (
                song_name VARCHAR(255),
                artist_name VARCHAR(255),
                time VARCHAR(255),
                timestamp TIMESTAMP,
                favorite_song INT,
                favorite_artist INT,
                daily_listening INT
            );
        """
    )

    
    
    run_elt = PythonOperator(
        task_id='run_elt',
        python_callable=elt_run,
        dag=dag
    )
    
    
    create_Spotify_Tracks_table >> run_elt
    
    
    