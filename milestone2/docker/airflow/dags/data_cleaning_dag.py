# Import necessary modules
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule

# Import the functions from the _functions package
from _functions.cleaning1 import (
    extract_and_clean_data,
    extract_state_data,
    combine_sources,
    load_to_db,
    handle_outliers,
    encode_categorical_features
)

# Define the default arguments
default_args = {
    "owner": "data_engineering_team",
    "depends_on_past": False,
    'start_date': days_ago(2),
    "retries": 0,
}

# Define the DAG
with DAG(
    'milestone2_project_dag',
    default_args = default_args,
    description='A pipeline for data cleaning and preprocessing',
    schedule_interval='@once',
    tags=['pipeline', 'etl', 'fintech'],
) as dag:
    
# Define the tasks

    # Define the start and end tasks 
    # These are empty tasks that are used to indicate the start and end of the DAG
    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')


    # Task to extract and clean the data
    extract_clean_task = PythonOperator(
        task_id='extract_clean',
        python_callable=extract_and_clean_data,  
        op_kwargs={
            'filename': '/opt/airflow/data/fintech_data_5_64_19288.csv',
            'output_path': '/opt/airflow/data/fintech_clean.parquet'
        }
    )


    # Task to extract state data
    extract_state_data_task = PythonOperator(
        task_id='extract_state_data',
        python_callable=extract_state_data,
        op_kwargs={
            'file_name': '/opt/airflow/data/states.csv',
            'output_path': '/opt/airflow/data/state_data.parquet'
        }
    )

    # Task to combine the sources
    combine_sources_task = PythonOperator(
        task_id='combine_sources',
        python_callable=combine_sources,
        op_kwargs={
            'main_file': '/opt/airflow/data/fintech_clean.parquet',
            'state_data': '/opt/airflow/data/state_data.parquet',
            'output_path': '/opt/airflow/data/combined_data.parquet'
        }
    )


    # Task to load the data to Postgres   
    load_to_postgres_task = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_to_db,
        op_kwargs={
            'filename': '/opt/airflow/data/combined_data.parquet',
            'table_name': 'fintech_clean',
            'postgres_opt': {
                'user': 'root',
                'password': 'root',
                'host': 'pgdatabase',
                'port': 5432,
                'db': 'data_engineering'
            }
        }
    )
    
    # Task to handle outliers
    handle_outliers_task = PythonOperator(
        task_id='handle_outliers',
        python_callable=handle_outliers,
        op_kwargs={
            'filename': '/opt/airflow/data/fintech_db_table.csv',
            'output_path': '/opt/airflow/data/fintech_handled.csv'
        }
    )
    
    # Task to encode categorical features
    encode_categorical_features_task = PythonOperator(
    task_id='encode_categorical_features',
    python_callable=encode_categorical_features,
    op_kwargs={
        'filename': '/opt/airflow/data/fintech_handled.csv',
        'output_path': '/opt/airflow/data/fintech_encoded.csv',
        'encoding_lookup_path': '/opt/airflow/data/encoding_lookup.csv'
    }
)

# Define the task dependencies for the DAG

# The order of the tasks is as follows: 
start >> [extract_clean_task, extract_state_data_task]

# Continue with parallel processing
extract_clean_task >> combine_sources_task
extract_state_data_task >> combine_sources_task

# Continue with sequential processing
combine_sources_task >> load_to_postgres_task
load_to_postgres_task >> handle_outliers_task
handle_outliers_task >> encode_categorical_features_task
encode_categorical_features_task >> end
