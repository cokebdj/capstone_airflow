from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.hooks.aws_hook import AwsHook
from operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries
from airflow.models import Variable


aws_hook = AwsHook("aws_credentials")
credentials = aws_hook.get_credentials()
AWS_KEY = credentials.access_key
AWS_SECRET = credentials.secret_key

s3_bucket = Variable.get('s3_bucket')
region = Variable.get('region')



default_args = {
    'owner': 'udacity',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False,
    'start_date': datetime(2019, 1, 12),
}

dag = DAG('udacity_capstone_project_005',
          catchup=False,
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *'
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_weather_raw_to_redshift = StageToRedshiftOperator(
    task_id='stage_weather_raw',
    dag=dag,
    redshift_conn_id="redshift",
    table="staging_weather",
    s3_bucket=s3_bucket,
    s3_key="weather",
    s3_access_key_id=AWS_KEY,
    s3_secret_access_key=AWS_SECRET,
    region=region,
    delimiter=',',
    create_query= SqlQueries.create_staging_weather
)

stage_bikes_raw_to_redshift = StageToRedshiftOperator(
    task_id='stage_bikes_raw',
    dag=dag,
    redshift_conn_id="redshift",
    table="staging_bikes",
    s3_bucket=s3_bucket,
    s3_key="bikes",
    s3_access_key_id=AWS_KEY,
    s3_secret_access_key=AWS_SECRET,
    region=region,
    delimiter=',',
    create_query= SqlQueries.create_staging_bikes
)

wait_operator = DummyOperator(task_id='waiting_until_completion',  dag=dag)

load_rides_facts_table = LoadFactOperator(
    redshift_conn_id="redshift",
    table="rides",
    create_query=SqlQueries.create_rides,
    insert_query=SqlQueries.rides_table_insert,
    task_id='Load_rides_facts_table',
    dag=dag
)

load_stations_dimension_table = LoadDimensionOperator(
    redshift_conn_id="redshift",
    table="stations",
    create_query=SqlQueries.create_stations,
    insert_query=SqlQueries.stations_table_insert,
    task_id='Load_stations_dim_table',
    dag=dag
)

load_weather_dimension_table = LoadDimensionOperator(
    redshift_conn_id="redshift",
    table="weather",
    create_query=SqlQueries.create_weather,
    insert_query=SqlQueries.weather_table_insert,
    task_id='Load_weather_dim_table',
    dag=dag
)


run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    redshift_conn_id="redshift",
    dag=dag
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> [stage_weather_raw_to_redshift, stage_bikes_raw_to_redshift] >> wait_operator >> [load_rides_facts_table, load_stations_dimension_table, load_weather_dimension_table] >> run_quality_checks >> end_operator