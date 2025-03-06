import cv2
import mediapipe as mp
import pyautogui
import time

def is_fist_closed(landmarks):
    tip_ids = [4, 8, 12, 16, 20]
    finger_folded = []
    
    for tip in tip_ids[1:]:  # Skiping thumb for now
        if landmarks[tip].y > landmarks[tip - 2].y:  # Finger tip is below the PIP joint
            finger_folded.append(True)
        else:
            finger_folded.append(False)
    
    return all(finger_folded)

# Initialize Mediapipe Hand Detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Open Camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip image for a mirror effect
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Check if hand is making a fist
            if is_fist_closed(hand_landmarks.landmark):
                print("Fist detected! Taking screenshot...")
                # filename = f"Screenshot_{int(time.time())}.png"
                # pyautogui.screenshot().save(filename)
                pyautogui.screenshot().save("Screenshot.png")
                cv2.waitKey(500)  # Small delay to prevent multiple triggers
    
    cv2.imshow("Screen Shot", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
