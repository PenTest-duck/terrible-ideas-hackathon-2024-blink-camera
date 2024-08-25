import cv2
from datetime import datetime
from pydub.playback import play
from scipy.spatial import distance as dist
from imutils import face_utils
import imutils
import dlib
from datetime import datetime, timedelta
import threading
import random
import arduino
from time import sleep

# Imports from local files
from s3 import uploadToS3
import arduino
from constants import *

# arduino.off()

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(SHAPE_PREDICTOR_MODEL_PATH)

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# start the video capture
print("[INFO] starting video capture...")
vs = cv2.VideoCapture(0)
vs.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
vs.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# loop over frames from the video stream
def main():
    time_prev = datetime.now()
    total_closed = 0
    consecutive_closed = 0
    consecutive_open = 0
    last_photo = None
    last_photo_time = datetime.now()
    avgEARHistory = []
    enabled = False
    flash_time = None

    while True:
        ret, frame_raw = vs.read()
        if not ret:
            continue

        if flash_time is not None and datetime.now() > flash_time:
            print("flashing")
            arduino.flash(100)
            flash_time = None

        if last_photo is not None: 
            modified_last_photo = last_photo.copy()
            cv2.putText(modified_last_photo, f"Press 1 to post online, 2 to try again", (10, 70), TEXT_FONT, TEXT_FONT_SCALE, TEXT_COLOR_BLUE, 5)
            cv2.imshow(DISPLAY_WINDOW_NAME, modified_last_photo)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("1"):
                if SHOULD_UPLOAD_IMAGES_TO_S3:
                    # Upload produced images to S3
                    print("Uploading image to S3 ... ", end="")
                    thread = threading.Thread(target = uploadToS3, args = [last_photo])
                    thread.start() # Use multithreading to not block the video stream
                
                # Write photo to local storage
                timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
                photoPath = SAVED_PHOTOS_PATH + timestamp + ".png"
                print(photoPath)
                cv2.imwrite(photoPath, last_photo)
                last_photo = None
            if key == ord("2"):
                last_photo = None

            continue

        # Grab the frame from the video stream, resize
        # it, and convert it to grayscale
        # channels)

        SF = 2
        #frame_large = imutils.resize(frame_raw, width=1440)
        frame_large = frame_raw.copy()
        frame = imutils.resize(frame_raw, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_large = cv2.cvtColor(frame_large, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = detector(gray, 0)

        # loop over the face detections
        closed_eyes_count = 0
        leftEAR = 0
        rightEAR = 0
        EARs = []
        for rect in rects:
            left = (rect.left() * 100) // 1280
            right = (rect.right() * 100) // 1280

            # arduino.set_region(left, right, 0x0000ff)

            rect_large = dlib.rectangle(rect.left() * SF, rect.top() * SF, rect.right() * SF, rect.bottom() * SF)
            cv2.rectangle(frame_large, (rect.left() * SF, rect.top() * SF), (rect.right() * SF, rect.bottom() * SF), (255, 0, 0))

            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray_large, rect_large)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            EARs.extend([leftEAR, rightEAR])

            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            leftClosed = False
            rightClosed = False
            if leftEAR < EYE_AR_THRESH:
                closed_eyes_count += 1
                leftClosed = True
            if rightEAR < EYE_AR_THRESH:
                closed_eyes_count += 1
                rightClosed = True

            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            leftColour = (0, 255, 0) if leftClosed else (0, 0, 255)
            rightColour = (0, 255, 0) if rightClosed else (0, 0, 255)
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame_large, [leftEyeHull], -1, leftColour, 1)
            cv2.drawContours(frame_large, [rightEyeHull], -1, rightColour, 1)

        canTakePhoto = len(rects) > 0 and closed_eyes_count >= 2 * len(rects)

        avgEAR = sum(EARs) / (2 * len(rects)) if len(rects) else None
        avgEARHistory.append(avgEAR)

        # draw the computed info on the frame
        cv2.putText(frame_large, f"Num Faces: {len(rects)}", (10, 30),
            TEXT_FONT, 0.7, (0, 0, 255), 2)
        cv2.putText(frame_large, f"Num Closed Eyes: {closed_eyes_count}", (10, 80),
            TEXT_FONT, 0.7, (0, 0, 255), 2)
        cv2.putText(frame_large, f"Can Capture: {canTakePhoto}", (10, 130),
            TEXT_FONT, 0.7, (0, 0, 255), 2)
        cv2.putText(frame_large, f"EARs: L {leftEAR:.2f} R {rightEAR:.2f}", (10, 180),
            TEXT_FONT, 0.7, (0, 0, 255), 2)
        
        mspf = (datetime.now() - time_prev) / timedelta(milliseconds=1)
        time_prev = datetime.now()
        cv2.putText(frame_large, f"FPS: {(1000 / mspf):.0f}", (10, 230),
            TEXT_FONT, 0.7, (0, 0, 255), 2)
        
        if enabled:
            cv2.putText(frame_large, "Taking Photo. Get Ready!",
                        TEXT_POSITION, TEXT_FONT, TEXT_FONT_SCALE,
                        TEXT_COLOR_RED, TEXT_THICKNESS, cv2.LINE_AA)

        if canTakePhoto:
            total_closed += 1
            consecutive_closed += 1
            consecutive_open = 0
        else:
            consecutive_closed = 0
            consecutive_open += 1

        if consecutive_open > RELEASE_FRAMES:
            total_closed = 0

        should_capture_immediate = False
        if avgEAR and len(avgEARHistory) >= 8 and all([x is not None for x in avgEARHistory[-8:]]):
            avgAvg = sum(avgEARHistory[-8:]) / 8
            if avgAvg - min(avgEARHistory[-8:]) > DELTA_IMMEDIATE and canTakePhoto:
                should_capture_immediate = True

        should_capture = (
            ((total_closed >= ATTACK_FRAMES_TOTAL and consecutive_closed >= ATTACK_FRAMES_CONSECUTIVE)
            or should_capture_immediate)
            and (datetime.now() - last_photo_time).total_seconds() > DELAY_TIME)

        if enabled and should_capture:
            last_photo_time = datetime.now()
            consecutive_closed = 0
            total_closed = 0

            # Make shutter noise
            thread = threading.Thread(target = play, args = [SHUTTER_SOUND])
            thread.start()

            last_photo = frame_raw
    
        # show the frame
        cv2.imshow(DISPLAY_WINDOW_NAME, frame_large)

        # arduino.show()

        # if the `q` key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord(" "):
            enabled = not enabled  # toggle
            #if enabled:
            #    arduino.slide_on()

        if key == ord("f"):
            flash_time = datetime.now() + timedelta(seconds=random.randint(0, MAX_FLASH_DELAY))
            print(f"flashing at {flash_time}")
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.release()

if __name__ == '__main__':
    main()
