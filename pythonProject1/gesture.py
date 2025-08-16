import cv2
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils

# 初始化手部模型
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
# 镜头
cap = cv2.VideoCapture(0)


def is_index_finger_up():


    ret, frame = cap.read()
    if not ret:
        return False

    frame = cv2.flip(frame,1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)



    if not results.multi_hand_landmarks:
        return False
    else:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow('Hand Detection', frame)

    for hand_landmarks in results.multi_hand_landmarks:
        # 獲取關鍵點坐標（食指指尖和指根）
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]  # 大拇指的指间关节（Interphalangeal Joint）
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
        middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
        ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
        ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
        pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
        pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]

        # 簡單邏輯：如果食指指尖的 y 坐標低於指根（向上伸出），且其他手指未伸出
        if index_tip.y < index_pip.y and thumb_tip.x > thumb_ip.x and middle_tip.y > middle_pip.y and ring_tip.y > ring_pip.y and pinky_tip.y > pinky_pip.y:
            return True

    return False

def release():
    cap.release()
    cv2.destroyAllWindows()