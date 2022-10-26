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

Inside the venv and the root directory of the project, create the file *settings.json* to save public setting and *.secrets.json*, which is added to *.gitigore* automatically:

`myconfig -i json`

### Create the Pub/Sub topic

1. Enable Pub/Sub API via the console or with `gcloud services enable pubsub.googleapis.com`
2. Create a service account with the Pub/Sub Admin role
3. Create a JSON key for the account and put in *settings.json* the path to the key generated
4. Execute the file setup/create_topic.py
