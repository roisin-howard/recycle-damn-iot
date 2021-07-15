# recycle-damn-iot

Hackathon 2021 Recycling Image Classification Project

To Do: Update readme properly.


# Set up pi

install the following:

``pip3 install setuptools``
``pip3 install tensorflow==1.13.1``
``pip3 install git+https://github.com/lobe/lobe-python``


# Clone repo

``git@github.com:roisin-howard/recycle-damn-iot.git``


# Run locally on pi

cd to recycle_damn_iot directory
``python3 src/recycle_damn_iot.py``

# Run BigQuery Data Stream
For the purpose of this hackathon we're using a private GCP project. The releavnt service account json has been sent to you beforehand. Before you can run the client you must first export the credentials to the local system's environment variables using the key GOOGLE_APPLICATION_CREDENTIALS. See here for more info - https://cloud.google.com/docs/authentication/getting-started

Once the system has access you can perform the following operations using the BigQueryClient:
* Init BigQuery Schema - Creates the dataset and table within the specified project ID if they don't exist
* Stream Data - Will stream a single row to the table in BigQuery. Prediction data must be populated into the Prediction model and sent to this method where it will be serialised and sent. The method will return True if successful and False if any errors occur. Inspection of the console will provide further detail of any errors.

Implementation examples can be found within ``test_data_stream.py``


