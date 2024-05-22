import os
import time
import cv2
import numpy as np
import logging
from opcua import Client

# Define a custom logging level
IMPORTANT = 25
logging.addLevelName(IMPORTANT, "IMPORTANT")

def important(self, message, *args, **kws):
    if self.isEnabledFor(IMPORTANT):
        self._log(IMPORTANT, message, args, **kws)

# Add the custom level to the Logger class
logging.Logger.important = important

# Set up logging to use the custom level
logging.basicConfig(level=IMPORTANT, format='%(asctime)s - %(levelname)s - %(message)s')

# Environment variables
OPC_SERVER_URL = os.getenv('OPC_SERVER_URL', 'opc.tcp://10.18.12.185:49324')
TAG_NAME = os.getenv('TAG_NAME', 'ns=2;s=PROCESSO.PLC.MACERACAO.TEMPERATURA_SUPERIOR_M2')
CAMERA_INDEX = int(os.getenv('CAMERA_INDEX', 0))
EQUIPMENT = os.getenv('EQUIPMENT', 'DECANTADOR')
VALID_STEPS = os.getenv('VALID_STEPS', "19.74,19.75,19.76,19.77,19.78,20.17,20.16,20.19,19.83,19.84")

# Convert VALID_STEPS from string to a list of floats
valid_steps = [float(step) for step in VALID_STEPS.split(',')]

# Base directory to save images
BASE_IMAGE_SAVE_PATH = '/data'

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def take_pictures(step):
    blank_image = np.zeros((480, 640, 3), dtype=np.uint8)
    directory_path = os.path.join(BASE_IMAGE_SAVE_PATH, EQUIPMENT, step)
    ensure_directory(directory_path)
    for i in range(3):
        timestamp = time.strftime("%d.%m.%Y_%H.%M.%S")
        image_path = os.path.join(directory_path, f'{timestamp}_{i}.png')
        cv2.imwrite(image_path, blank_image)
        logging.getLogger().important(f"Image saved: {image_path}")
        time.sleep(2)

class SubHandler(object):
    def __init__(self):
        self.last_value = None  # Initialize a variable to store the last value that triggered pictures

    def datachange_notification(self, node, val, data):
        rounded_val = round(float(val), 1)
        logging.getLogger().important(f"Data change on {node}: New value = {rounded_val}")

        # Check if the new value is different from the last value
        if rounded_val != self.last_value:
            if rounded_val in valid_steps:
                logging.getLogger().important("Value within the valid steps, taking pictures.")
                take_pictures(str(rounded_val))
                self.last_value = rounded_val  # Update the last value to the current value
            else:
                logging.getLogger().important("Value not within the valid steps.")
        else:
            # If the value hasn't changed, log this information or simply do nothing
            logging.getLogger().important("Value unchanged, no new pictures taken.")


def main():
    client = Client(OPC_SERVER_URL)
    try:
        client.connect()
        logging.getLogger().important(f"Connected to {OPC_SERVER_URL}")
        tag_node = client.get_node(TAG_NAME)
        handler = SubHandler()
        sub = client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(tag_node)
        logging.getLogger().important("Subscription created, waiting for events...")
        while True:
            time.sleep(1)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        client.disconnect()
        logging.getLogger().important("Client disconnected.")

if __name__ == '__main__':
    main()
