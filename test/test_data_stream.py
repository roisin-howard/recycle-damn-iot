import sys
sys.path.append('../')

from data_stream.BigQueryClient import BigQueryClient
from models.prediction import Prediction
from uuid import uuid4
from datetime import datetime
import random

# # Warehouse schema variables
project_id = "hackathon-recycler-damn-iot"
dataset_name = "recycler_dataset"
table_name = "predictions_raw"
schema_def = []
test_predictions = ['paper', 'plastic', 'glass']

# # Initialise the warehouse schema
client = BigQueryClient()
client.init_schema(project_id, dataset_name, table_name, schema_def)


# Stream a single record
pred = Prediction()
pred.set_id(random.randrange(0,500))
pred.set_device_id("76a9d75c-ff0f-476c-a2fd-c6ba7855cb05")
pred.set_prediction(random.choice(test_predictions))
pred.set_accuracy(random.uniform(0, 100))
pred.set_prediction_datetime(datetime.utcnow())

client.stream_data(project_id, dataset_name, table_name, pred)

