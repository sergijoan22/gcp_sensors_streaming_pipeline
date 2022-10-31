# Streaming pipeline in Google Cloud
Streaming pipeline using Google Cloud services.

## Setup

### Create a virtual environment for Python in local

Following https://cloud.google.com/python/docs/setup.

In the terminal, go to the project folder:

`cd gcp_sensors_streaming_pipeline`

Create the virtual environment:

`py -m venv env`

To use it:

`.\env\Scripts\activate`

Install the packages needed:

```
pip install -r requirements.txt
```

To exit:

`deactivate`

### Create file with global variables

Use of the [library myconfig](https://pypi.org/project/myconfig/) to generate two files where global variables are used.

Inside the venv and the root directory of the project, create the file *settings.json* to save public setting and *.secrets.json*, which is added to *.gitignore* automatically:

`myconfig -i json`

### Create the Pub/Sub topic

1. Enable Pub/Sub API via the console or with `gcloud services enable pubsub.googleapis.com`
2. Create a service account with the Pub/Sub Admin role
3. Create a JSON key for the account and put in *settings.json* the path to the key generated
4. Execute the file *setup/create_topic.py*

### Read the Pub/Sub topic from the local machine

1. Execute *setup/create_subscription.py* to create a pull subscription to the topic
2. Execute *data_generator/read_data.py* to read messages from the topic

### Publish directly from Pub/Sub to BigQuery

Publish messages from Pub/Sub to BigQuery.
First, give the service account used by Pub/Sub a role to edit in BigQuery
Create a table with:

```sql
CREATE OR REPLACE TABLE prueba.topic_ps (
  subscription_name STRING,
  message_id STRING,
  publish_time TIMESTAMP,
  data STRING,
  attributes STRING)
OPTIONS(
  description="subscriber of the raw pubSub messages"
)
```

### Run Dataflow

1. Create a variable with the project in the shell

	```bash
	export PROJECT=$(gcloud config get-value project)
	export REGION=europe-southwest1
	```

2. Create a bucket with the name of the project

	```bash
	gsutil mb -c regional -l europe-southwest1 gs://$PROJECT
	```

3. Upload the file with the Dataflow code to the GCS bucket

4. Copy the file from the GCS bucket to the shell

	```bash
	gsutil -m cp -R gs://prueba-sj22/data_ingestion.py dataflow/data_ingestion.py
	```

5. Run a docker with Python 3.7. The PROJECT_ID variable is passed, and a volume between the host and the container is done to read the Dataflow file.

	```bash
	docker run -it -e PROJECT_ID=$PROJECT_ID -e REGION=$REGION -v $(pwd)/dataflow:/dataflow python:3.7 /bin/bash
	```

6. Install Beam. The version 2.33.0 is used in this case

	```
	apache-beam[gcp,test]==2.33.0
	```

7. Run the Beam job in Dataflow

	```
	python data_ingestion.py \
	    --project=gcp_project_id \
	    --region=$REGION \
	    --input_topic=projects/gcp_project_id/topics/my-id \
	    --output_path=gs://$PROJECT_ID/samples/output \
	    --runner=DataflowRunner \
	    --window_size=2 \
	    --num_shards=2 \
	    --temp_location=gs://$PROJECT_ID/temp
	```

	
