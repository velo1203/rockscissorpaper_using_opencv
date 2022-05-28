import cv2
import mediapipe as mp
import os

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    img_height, img_width, _ = image.shape


    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        
        thumb_finger_state = 0
        if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y * img_height > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y * img_height:
            if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y * img_height > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y * img_height:
                if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y * img_height > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * img_height:
                    thumb_finger_state = 1

        index_finger_state = 0
        if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * img_height > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * img_height:
            if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * img_height > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * img_height:
                if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * img_height > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * img_height:
                    index_finger_state = 1

        middle_finger_state = 0
        if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * img_height > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * img_height:
            if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * img_height > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * img_height:
                if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * img_height > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * img_height:
                    middle_finger_state = 1


        ring_finger_state = 0
        if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y * img_height > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * img_height:
            if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * img_height > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y * img_height:
                if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y * img_height > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * img_height:
                    ring_finger_state = 1

        pinky_finger_state = 0
        if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y * img_height > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y * img_height:
            if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y * img_height > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y * img_height:
                if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y * img_height > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * img_height:
                    pinky_finger_state = 1

        text = 'FIND ERROR'
        if index_finger_state == 1 and middle_finger_state == 1 and ring_finger_state == 0 and pinky_finger_state == 0:
            text = 'Scissors'
        if index_finger_state == 0 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 0:
            text = 'Rock'
        if index_finger_state == 1 and middle_finger_state == 1 and ring_finger_state == 1 and pinky_finger_state == 1:
            text = 'Paper'


        # os.system('cls')
        # if middle_finger_state == 1:
        #     print('middle finger 펴짐')
        # if ring_finger_state == 1:
        #     print('ring finger 펴짐')
        # if pinky_finger_state == 1:
        #     print('pinky finger 펴짐')

        cv2.putText(image,text, (10,20),cv2.FONT_HERSHEY_SIMPLEX,
        1, (0,0,255),3)


        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())


    cv2.imshow('MediaPipe Hands',image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
