from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 create_query="",
                 insert_query="",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.create_query = create_query
        self.insert_query = insert_query

    def execute(self, context):
        
        self.hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.hook.run(self.create_query)
        self.log.info(f'Table {self.table} created.')
        
        self.hook.run(f""" INSERT INTO {self.table} ({self.insert_query}) ;""")
        self.log.info(f'Table {self.table} filled.')
