from cv2 import FONT_HERSHEY_SIMPLEX
from pydub import AudioSegment

# This flag allows uploading images to a public S3 bucket
# When enabling this, don't forget to supply the credentials 
# AWS_PROFILE="Terrible Hackathon" python3 main.py
SHOULD_UPLOAD_IMAGES_TO_S3 = True

# This flag allows triggering the flash etc. through the Arduino
SHOULD_USE_ARDUINO = True

SAVED_PHOTOS_PATH = "./photos/"
SHUTTER_SOUND_PATH = "./assets/camera-shutter-sound.mp3"
SHUTTER_SOUND = AudioSegment.from_mp3(SHUTTER_SOUND_PATH)
SHAPE_PREDICTOR_MODEL_PATH = "./model/shape_predictor_68_face_landmarks.dat"

SF = 2
EYE_AR_THRESH = 0.19           # maximum EAR value for closed eyes
ATTACK_FRAMES_TOTAL = 3        # num total closed frames needed to take photo
ATTACK_FRAMES_CONSECUTIVE = 2  # num consecutive closed frames needed
RELEASE_FRAMES = 5             # num consecutive open frames needed to reset
DELAY_TIME = 3                 # wait 3s before next photo
DELTA_IMMEDIATE = 0.1          # if EAR decreases by > this much in some time
                               # period then a photo is taken

MAX_FLASH_DELAY = 3 # seconds
PHOTO_REVIEW_SECONDS = 3

DISPLAY_WINDOW_NAME = "Camera Preview"
TEXT_POSITION = (300, 70)
TEXT_FONT = FONT_HERSHEY_SIMPLEX
TEXT_FONT_SCALE = 2.0
TEXT_COLOR_RED = (0, 0, 255)
TEXT_COLOR_GREEN = (0, 255, 0)
TEXT_COLOR_BLUE = (255, 0, 0)
TEXT_THICKNESS = 2