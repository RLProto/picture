import cv2

def capture_image():
    # Start capturing video input from the webcam
    cap = cv2.VideoCapture(0)  # The argument 0 indicates /dev/video0

    # Set resolution to 1920x1080 or the maximum supported by your camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    if not cap.isOpened():
        print("Cannot open the video device")
        return
    
    # Read a frame from the webcam, ret is a boolean for success/failure
    ret, frame = cap.read()

    if ret:
        # Save the captured image to a file
        cv2.imwrite('captured_image.jpg', frame)
        print("Image saved successfully")
    else:
        print("Failed to capture image")

    # Release the camera and close all windows
    cap.release()

if __name__ == "__main__":
    capture_image()
