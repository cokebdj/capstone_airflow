from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 s3_access_key_id="",
                 s3_secret_access_key="",
                 region="",
                 create_query="",
                 delimeter="",
                 *args, **kwargs):
        
        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.s3_access_key_id = s3_access_key_id
        self.s3_secret_access_key = s3_secret_access_key
        self.region = region
        self.delimeter = delimeter 
        self.create_query = create_query

        
    def execute(self, context):
        
        self.hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
                
        self.hook.run(self.create_query)
        self.log.info(f'Table {self.table} created.')
        
        copy_query_statement = f"""
                               COPY {self.table}
                               FROM 's3://{self.s3_bucket+'/'+self.s3_key}'
                               ACCESS_KEY_ID '{self.s3_access_key_id}'
                               SECRET_ACCESS_KEY '{self.s3_secret_access_key}'
                               DELIMETER '{self.delimeter}'
                               REGION '{self.region}';
                               """
        
        self.hook.run(copy_query_statement)
        self.log.info(f'Table {self.table} filled.')



