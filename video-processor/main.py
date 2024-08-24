import cv2
from datetime import datetime
from time import time

SAVED_PHOTOS_PATH = "./photos/"

ATTACK_FRAMES_TOTAL = 1        # num total closed frames needed to take photo
ATTACK_FRAMES_CONSECUTIVE = 1  # num consecutive closed frames needed
RELEASE_FRAMES = 1            # num consecutive open frames needed to reset

TEXT_POSITION = (70, 70)
TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_FONT_SCALE = 2.0
TEXT_COLOR_RED = (0, 0, 255)
TEXT_COLOR_GREEN = (0, 255, 0)
TEXT_THICKNESS = 2
SECONDS_DISPLAY_PHOTO_TAKEN_MSG = 2

STATE_DETECTING = 0
STATE_TAKING_PHOTO = 1
STATE_FINISH_PHOTO = 2

# Load Haar cascade classifiers
# Cascade classifiers are a set of simple detectors which individually check for features that surmount to detect larger, more abstract features
# Here we load cascade classifiers for detecting faces and eyes
faceCascadePath = "./Model/haarcascade_frontalface_alt.xml"
eyesCascadePath = "./Model/haarcascade_eye_tree_eyeglasses.xml"
faceCascade = cv2.CascadeClassifier(faceCascadePath)
eyesCascade = cv2.CascadeClassifier(eyesCascadePath)

# Start capturing video from laptop camera (0)
print("Starting video capture from camera...")
cam = cv2.VideoCapture(0)

total_closed = 0
consecutive_closed = 0
consecutive_open = 0

state = STATE_DETECTING
lastPhotoTakenTime = time()

while True:
    # Debugging statements if needed
    # print(f"tc: {total_closed}, cc: {consecutive_closed}, co: {consecutive_open}")

    # Try to read a single frame of image from the camera
    ret, image = cam.read()
    if not ret:
        continue # wait for next frame

    # We convert the image to greyscale for easier detection
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = faceCascade.detectMultiScale(
        frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        # flags = cv2.CASCADE_SCALE_IMAGE
    )

    rawImage = image.copy()
    facesCount = 0
    eyesCount = 0
    for (x, y, w, h) in faces:
        facesCount += 1

        # Draw rectangles around the faces
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Now take just the face as the frame to be detected for the eyes
        roi_gray = frame[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]

        # Detect the eyes within the face
        eyes = eyesCascade.detectMultiScale(roi_gray)

        # Draw rectangles around the eyes
        for (ex, ey, ew, eh) in eyes:
            eyesCount += 1
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    if state == STATE_TAKING_PHOTO:
        cv2.putText(image, "Taking Photo. Get Ready!", TEXT_POSITION, TEXT_FONT, TEXT_FONT_SCALE, TEXT_COLOR_RED, TEXT_THICKNESS, cv2.LINE_AA)
    elif state == STATE_FINISH_PHOTO:
        cv2.putText(image, "Photo taken!", TEXT_POSITION, TEXT_FONT, TEXT_FONT_SCALE, TEXT_COLOR_GREEN, TEXT_THICKNESS, cv2.LINE_AA)
        if time() - lastPhotoTakenTime >= SECONDS_DISPLAY_PHOTO_TAKEN_MSG:
            state = STATE_DETECTING


    # Display the parsed image on a window
    cv2.imshow("Camera output", image)

    # Photo can be taken when there are non-zero faces and zero eyes
    eyesClosed = facesCount > 0 and eyesCount == 0

    if eyesClosed:
        total_closed += 1
        consecutive_closed += 1
        consecutive_open = 0
    else:
        consecutive_closed = 0
        consecutive_open += 1

    if consecutive_open > RELEASE_FRAMES:
        total_closed = 0

    should_capture = (total_closed > ATTACK_FRAMES_TOTAL
        and consecutive_closed > ATTACK_FRAMES_CONSECUTIVE)
    
    if state == STATE_TAKING_PHOTO and should_capture:
        consecutive_closed = 0
        total_closed = 0

        print("Taking photo...")
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        photoPath = SAVED_PHOTOS_PATH + timestamp + ".png"
        cv2.imwrite(photoPath, rawImage)

        lastPhotoTakenTime = time()
        state = STATE_FINISH_PHOTO

    key = cv2.waitKey(1) & 0xFF
    if key == ord('p'):
        state = STATE_TAKING_PHOTO
    elif key == ord('q'):
        break

# Gracefully shut down the video output window and the camera
print("Shutting down the camera.")
cv2.destroyAllWindows()
cam.release()