import cv2
import mediapipe as mp
import pygame

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Initialize Pygame
pygame.init()
sound = pygame.mixer.Sound("sound.mp3")
sound.play()
sound.set_volume(0.5)  # Set initial volume
is_playing = True  # Track if sound is playing

# Function to detect gestures
def detect_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    # Check if all fingers are open (open palm)
    if (index_tip.y < thumb_tip.y and
        middle_tip.y < thumb_tip.y and
        ring_tip.y < thumb_tip.y and
        pinky_tip.y < thumb_tip.y):
        return "Open Palm"
    # Detect thumb up
    elif thumb_tip.y < index_tip.y:
        return "Thumb Up"
    # Detect index finger up
    elif index_tip.y < thumb_tip.y:
        return "Index Finger Up"
    else:
        return "No Gesture"

# Function to adjust volume and play/pause
def control_sound(gesture):
    global is_playing

    if gesture == "Thumb Up":
        sound.set_volume(min(1.0, sound.get_volume() + 0.1))  # Increase volume
    elif gesture == "Index Finger Up":
        sound.set_volume(max(0.0, sound.get_volume() - 0.1))  # Decrease volume
    elif gesture == "Open Palm":
        if is_playing:
            sound.stop()  # Pause the sound
            is_playing = False
        else:
            sound.play()  # Resume the sound
            is_playing = True

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Process the image and detect hands
    results = hands.process(image)

    # Convert the image back to BGR for rendering
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Draw hand landmarks and detect gestures
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = detect_gesture(hand_landmarks)
            control_sound(gesture)  # Control sound based on gesture

            # Display the detected gesture on the screen
            cv2.putText(image, f"Gesture: {gesture}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the image
    cv2.imshow('Hand Gesture Sound Control', image)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
pygame.quit()