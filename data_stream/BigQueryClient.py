from google.api_core.exceptions import Conflict
from google.cloud import bigquery

class BigQueryClient():
    '''
    Operations conducted against the data warehoue
    '''

    client = None
    location = "US"

    def __init__(self):
        self.client = bigquery.Client()

    def init_schema(self, project_id, dataset_name, table_name, schema_def):
        '''
        Initialise the schema in the data warehouse
        '''

        dataset_status = self.create_dataset(project_id, dataset_name)
        if dataset_status == False:
            print(f"Dataset {dataset_name} already exists in project {project_id}")
        else:
            print(f"Dataset {dataset_name} created in project {project_id}")

        table_status = self.create_table(project_id, dataset_name, table_name, schema_def)
        if table_status == False:
            print(f"Table {table_name} already exists in dataset {dataset_name}")
        else:
            print(f"Table {table_name} created in dataset {dataset_name}")


    def create_dataset(self, project_id, dataset_name):
        '''
        Create an individual dataset within the specified project
        '''

        try:
            dataset_id = f"{project_id}.{dataset_name}"
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = self.location

            dataset = self.client.create_dataset(dataset, timeout=30)
            return True
        except Conflict:
            return False

    def create_table(self, project_id, dataset_name, table_name, schema_def):
        '''
        Create an individual table within the specified dataset
        '''

        try:
            table_id = f"{project_id}.{dataset_name}.{table_name}"

            # TODO: Replace static schema with schema object
            schema = [
                bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
                bigquery.SchemaField("device_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("pred_label", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("pred_accuracy", "FLOAT64", mode="REQUIRED"),
                bigquery.SchemaField("pred_datetime", "DATETIME", mode="REQUIRED")
            ]

            table = bigquery.Table(table_id, schema=schema)
            table = self.client.create_table(table)
            return True
        except Conflict:
            return False

    def stream_data(self, project_id, dataset_name, table_name, data):
        '''
        Will insert a collection of records into the specified warehouse table
        '''

        try:
            table_id = f"{project_id}.{dataset_name}.{table_name}"

            rows_to_insert = [
                {
                    u"id": data.get_id(),
                    u"device_id": data.get_device_id(),
                    u"pred_label": data.get_prediction(),
                    u"pred_accuracy": data.get_accuracy(),
                    u"pred_datetime": str(data.get_prediction_datetime())
                }
            ]

            errors = self.client.insert_rows_json(
                table_id, rows_to_insert
            )

            if errors == []:
                print(f"Record {data.get_id()} has been streamed to table {table_name}")
                return True
            else:
                print(f"Errors: {errors}")
                return False
        except Exception as e:
            print(f"Errors writing data to table {table_name}. Exception [{e}]")
            return False