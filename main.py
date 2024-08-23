import cv2

# Load Haar cascade classifiers
# Cascade classifiers are a set of simple detectors which individually check for features that surmount to detect larger, more abstract features
# Here we load cascade classifiers for detecting faces and eyes
faceCascadePath = "./Model/haarcascade_frontalface_alt.xml"
eyesCascadePath = "./Model/haarcascade_eye_tree_eyeglasses.xml"
faceCascade = cv2.CascadeClassifier(faceCascadePath)
eyesCascade = cv2.CascadeClassifier(eyesCascadePath)

# Start capturing video from laptop camera (0)
print("Start video capture from camera...")
cam = cv2.VideoCapture(0) 

while True:
  # Read a single frame of image from the camera
  ret, image = cam.read()
  if not ret:
    break

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
  
  if facesCount > 0 and eyesCount == 0:
    print("Can take photo!")

  # Display the parsed image on a window
  cv2.imshow("Camera output", image)

  # Exit loop after 1 second delay if 'q' is pressed
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# Gracefully shut down the video output window and the camera
print("Shutting down the camera...")
cv2.destroyAllWindows()
cam.release()