# ???
import base64
import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5,min_tracking_confidence=0.5)

def detect_hand(image):
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


  results = hands.process(image)

  # Draw the hand annotations on the image.
  image.flags.writeable = True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  image_height, image_width, _ = image.shape
  xy = (-1,-1)
  if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
          mp_drawing.draw_landmarks(
                                    image,
                                    hand_landmarks,
                                    mp_hands.HAND_CONNECTIONS,
                                    mp_drawing_styles.get_default_hand_landmarks_style(),
                                    mp_drawing_styles.get_default_hand_connections_style())
          
          # print("mark: ", str(hand_landmarks))
          # print(
          # f'Index finger tip coordinates: (',
          # f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          # f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
          # )
          # for m in hand_landmarks.landmark:
          #   print(m.x,m.y,m.z)
          m = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
          xy = int(m.x*image_width),int(m.y*image_height)
          # print("index finger: ",xy)
  return image,xy

def test0():
  cap = cv2.VideoCapture(0)
  while cap.isOpened():
    success, image = cap.read()
    # _, buffer = cv2.imencode('.jpg', image)

# Convert to base64 encoding and show start of data
    # jpg_as_text = base64.b64encode(buffer)
    # jpg_as_np = np.fromstring(base64.b64decode(jpg_as_text), dtype=np.uint8)
    # img = cv2.imdecode(jpg_as_np, cv2.IMREAD_COLOR)
    # cv2.imshow('img',img)
    # cv2.waitKey(5)

    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue
    image.flags.writeable = False
    image = detect_hand(image)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
  cap.release()

if __name__ == '__main__':
  test0()