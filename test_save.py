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
    directory_path = os.path.join(BASE_IMAGE_SAVE_PATH, EQUIPMENT, 'test_capture')
    ensure_directory(directory_path)
    
    # Initialize video capture
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        logging.error("Failed to open video device.")
        return False


    #cap.set(cv2.CAP_PROP_AUTO_WB,0)
    cap.set(cv2.CAP_PROP_WB_TEMPERATURE,2000)

    # Set the camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_WB_TEMPERATURE,2000)
    
    # Try capturing a frame to see if the resolution is set
    ret, frame = cap.read()
    if not ret:
        logging.error("Failed to capture image from camera.")
        cap.release()
        return False

    # Log the actual resolution obtained
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    logging.info(f"Attempting to capture at resolution: 1920x1080, Actual resolution: {actual_width}x{actual_height}")

    # Proceed with capturing and saving the image
    timestamp = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
    image_path = os.path.join(directory_path, f'{timestamp}.png')
    if cv2.imwrite(image_path, frame):
        logging.info(f"Image successfully saved: {image_path}")
    else:
        logging.error("Failed to save image using cv2.imwrite.")
    cap.release()
    return True


if __name__ == "__main__":
    result = take_picture()
    if result:
        logging.info("Image capture and save test completed successfully.")
    else:
        logging.info("Image capture and save test failed.")
