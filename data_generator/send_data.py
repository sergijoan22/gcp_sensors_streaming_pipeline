from datetime import datetime
from re import X
import time
import random
import json
from google.cloud import pubsub_v1
from myconfig import MyConfig
import os


# VARIABLES
sensors_info_location = r"data_generator/sensors_info.json"

# RANGE OF MAGNITUDE VALUES
temp_range = [-10,50]
light_range = [100,1000]
noise_range = [0,70]

# READ JSON WITH THE DEVICES INFO
devices_file = open(sensors_info_location, "r")
devices_file_content = devices_file.read()
devices_file.close()
devices = json.loads(devices_file_content)

# CREATES FUNCTION TO SEND DEVICE DATA
def data_generator(devices):
    data = {}
    # read number of devices
    n_devices = len(devices)
    # take a random device
    x_device = random.randint(0, n_devices - 1)
    # id from device
    data["device_id"] = devices[x_device]['device_id']
    # type from device
    device_type = devices[x_device]['type_id']
    data["device_type"] = device_type 
    if (device_type == 'Temperature'):
        data["value"] =  round(random.uniform(temp_range[0], temp_range[1]), 2)
    if (device_type == 'Light'):
        data["value"] =  round(random.uniform(light_range[0], light_range[1]), 2)
    if (device_type == 'Noise'):
        data["value"] =  round(random.uniform(noise_range[0], noise_range[1]), 2)
    data["timestamp"] = str(datetime.now())
    return data

# CONFIGURE PUBSUB
config = MyConfig(['settings.json', '.secrets.json'])
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.pubsub_admin_key_path

project_id = config.project_id
topic_id = config.topic_id

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)





# EXECUTE THE SIMULATION
if __name__ == "__main__":
   while True:
    # prepare the messages parts to be sent
    data = str(data_generator(devices)["value"]).encode('utf-8')
    att_sensor_id = str(data_generator(devices)["device_type"])  # attribute
    att_sensor_type = str(data_generator(devices)["device_id"])  # attribute
    att_timestamp = str(data_generator(devices)["timestamp"])  # attribute
    attributes = {
        "sensor_id": att_sensor_id,
        "sensor_type": att_sensor_type,
        "timestamp": att_timestamp
    }
    
    future = publisher.publish(
        topic_path, data, **attributes) # **attributes unpacks the dict to send each part as argument
    print("Published message id {}".format(future.result()))
    time.sleep(random.uniform(0.01, 0.2))