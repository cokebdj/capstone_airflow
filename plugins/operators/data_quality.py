from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = ['staging_weather','staging_bikes', 'rides', 'stations', 'weather']

    def execute(self, context):
        
        self.hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        for table in self.tables:
            self.log.info(f'Query for table {self.table}.')
            query = f"""  SELECT COUNT(*) FROM {table};  """
            records = self.hook.get_records(query)
            if records is None or len(records[0])<1:
                self.log.error(f'No records in table {self.table}.')
            else:
                self.log.info(f'Total of {records[0][0]} records in table {self.table}.')
                