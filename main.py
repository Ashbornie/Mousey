import cv2
import mediapipe as mp
import numpy as np
from pynput.mouse import Controller, Button

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Initialize the mouse controller
mouse = Controller()

# Open the webcam
cap = cv2.VideoCapture(0)

# Screen resolution
screen_width, screen_height = 1920, 1080
# Get the screen size

# Function to calculate the distance between two points
def calculate_distance(point1, point2):
    return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

# Variables for click and drag
dragging = False
drag_started = False
start_position = None
pinch_threshold = 0.06  # Adjust pinch threshold as needed (higher value for longer pinch)

# Variables for scrolling
scrolling = False
scroll_start_position = None
scroll_sensitivity = 0.01  # Adjust scroll sensitivity as needed

# Variables to store previous finger positions
prev_index_finger_tip_coords = None
prev_thumb_tip_coords = None

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the image horizontally for a later selfie-view display
    image = cv2.flip(image, 1)
    # Convert the BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and detect the hands
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            # Get hand label (left or right)
            hand_label = handedness.classification[0].label

            # Get landmarks for index finger tip, thumb tip, and middle finger tip
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            # Calculate coordinates for drawing (scaled to screen resolution)
            h, w, _ = image.shape
            index_finger_tip_coords = (int(index_finger_tip.x * w), int(index_finger_tip.y * h))
            thumb_tip_coords = (int(thumb_tip.x * w), int(thumb_tip.y * h))

            if hand_label == "Right":
                # Draw a green dot on the right index finger tip
                cv2.circle(image, index_finger_tip_coords, 10, (0, 255, 0), -1)

                # Draw a green dot on the right thumb tip
                cv2.circle(image, thumb_tip_coords, 10, (0, 255, 0), -1)

                # Convert the normalized coordinates to screen coordinates
                x = int(index_finger_tip.x * screen_width)
                y = int(index_finger_tip.y * screen_height)

                # Only update mouse position if there's a significant movement
                if prev_index_finger_tip_coords is not None:
                    # Calculate distance moved
                    movement_distance = calculate_distance(index_finger_tip, prev_index_finger_tip_coords)
                    if movement_distance > 0.005:  # Adjust threshold as needed
                        mouse.position = (x, y)
                else:
                    mouse.position = (x, y)

                # Update previous finger position
                prev_index_finger_tip_coords = index_finger_tip

                # Check if right thumb and index are pinched (scrolling)
                if calculate_distance(thumb_tip, index_finger_tip) < 0.05:
                    if not scrolling:
                        scrolling = True
                        scroll_start_position = (x, y)
                else:
                    if scrolling:
                        scrolling = False
                        scroll_start_position = None

                if scrolling:
                    # Calculate scroll amount based on vertical movement
                    scroll_delta = int(scroll_sensitivity * (scroll_start_position[1] - y))
                    mouse.scroll(0, scroll_delta)

            elif hand_label == "Left":
                # Draw blue dots on the left index finger tip and thumb tip
                cv2.circle(image, index_finger_tip_coords, 10, (255, 0, 0), -1)
                cv2.circle(image, thumb_tip_coords, 10, (255, 0, 0), -1)

                # Calculate the distance between the thumb tip and the index finger tip
                distance = calculate_distance(thumb_tip, index_finger_tip)

                # Check for pinch (click) gesture with delay for click and drag (dragging)
                if distance < pinch_threshold:
                    if not drag_started:
                        drag_started = True
                        start_position = (x, y)
                        mouse.press(Button.left)
                else:
                    if drag_started:
                        drag_started = False
                        mouse.release(Button.left)

                if drag_started:
                    # If currently dragging, move the cursor while holding the left button
                    mouse.position = (x, y)

    # Display the image
    cv2.imshow('Hand Tracking', image)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
