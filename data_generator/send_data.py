from datetime import datetime
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
    # returns magnitudes
    data["temp"] = 0
    data["humid"] = 0
    data["light"] = 0
    data["noise"] = 0    
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
    #print(data_generator(devices))
    # send the message
    data = str(data_generator(devices)["value"]).encode('utf-8')
    future = publisher.publish(
        topic_path, data)
    print("Published message id {}".format(future.result()))
    time.sleep(random.uniform(0.001 * 10, 0.2 * 10))