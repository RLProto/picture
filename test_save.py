import os
import cv2
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
CAMERA_INDEX = 0  # Typically 0 for the first connected camera
BASE_IMAGE_SAVE_PATH = './data'
EQUIPMENT = 'DECANTADOR'

def ensure_directory(path):
    """Ensure target directory exists; create if it does not."""
    if not os.path.exists(path):
        os.makedirs(path)
        logging.debug(f"Directory created: {path}")
    else:
        logging.debug(f"Directory already exists: {path}")

def take_picture():
    """Captures a single picture and saves it to a file."""
    directory_path = os.path.join(BASE_IMAGE_SAVE_PATH, EQUIPMENT, 'test_capture')
    ensure_directory(directory_path)
    
    # Start video capture
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        logging.error("Failed to open video device.")
        return False

    try:
        ret, frame = cap.read()
        if ret:
            timestamp = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
            image_path = os.path.join(directory_path, f'{timestamp}.png')
            if cv2.imwrite(image_path, frame):
                logging.info(f"Image successfully saved: {image_path}")
            else:
                logging.error("Failed to save image using cv2.imwrite.")
            return True
        else:
            logging.error("Failed to capture image from camera.")
            return False
    except Exception as e:
        logging.error(f"An exception occurred while capturing or saving the image: {e}")
        return False
    finally:
        cap.release()

if __name__ == "__main__":
    result = take_picture()
    if result:
        logging.info("Image capture and save test completed successfully.")
    else:
        logging.info("Image capture and save test failed.")
