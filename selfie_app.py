"""
Peace-sign Selfie App (standalone)

Usage:
  - Install dependencies: see requirements.txt or run
      pip install mediapipe opencv-python numpy
  - Run in PowerShell:
      python selfie_app.py
  - Show a ✌️ (index+middle fingers up, ring+pinky down). The app shows a 2-second countdown, takes a selfie, saves it with a timestamp, applies a filter, and displays the filtered image.

Notes:
  - Optimized for local execution on Windows. Uses winsound beep on Windows when available.
  - Keeps detection lightweight: reduced model complexity and optional frame-skip.

"""

import cv2
import numpy as np
import mediapipe as mp
import time
import os
from datetime import datetime
import platform

# Try to import winsound for a simple beep on Windows
try:
    if platform.system().lower().startswith('win'):
        import winsound
    else:
        winsound = None
except Exception:
    winsound = None

# --- Configuration ---
SAVE_DIR = os.path.abspath(os.path.dirname(__file__))
FILTER = 'sepia'  # 'grayscale', 'sepia', 'cartoon', or None
DELAY_SECONDS = 2
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
MODEL_COMPLEXITY = 0  # lower -> faster, higher -> more accurate
MAX_HANDS = 1
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.5
FRAME_SKIP = 0  # process every (FRAME_SKIP+1) frames; 0 -> process every frame
COOLDOWN_AFTER_CAPTURE = 2.0  # seconds to wait after a capture

# Mediapipe helpers
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Finger tips and pip (proximal interphalangeal) indices
TIP_IDS = [4, 8, 12, 16, 20]

# --- Utility functions ---

def timestamp_filename(basename='selfie', ext='jpg'):
    t = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{basename}_{t}.{ext}"


def apply_filter(img, mode='sepia'):
    """Apply a simple filter to a BGR OpenCV image and return BGR image."""
    if mode == 'grayscale':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    elif mode == 'sepia':
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        img_sepia = cv2.transform(img, kernel)
        img_sepia = np.clip(img_sepia, 0, 255).astype(np.uint8)
        return img_sepia
    elif mode == 'cartoon':
        img_color = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.medianBlur(img_gray, 7)
        edges = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 2)
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        cartoon = cv2.bitwise_and(img_color, edges_colored)
        return cartoon
    else:
        return img


def is_finger_up(landmarks, tip_idx, pip_idx):
    """Return True if the finger tip is above (smaller y) its pip joint in normalized coordinates."""
    return landmarks.landmark[tip_idx].y < landmarks.landmark[pip_idx].y


def detect_peace_sign(hand_landmarks):
    """Return True if index and middle fingers are up and ring+pinky down. Also check finger separation.

    hand_landmarks: mediapipe normalized landmarks
    """
    try:
        idx_up = is_finger_up(hand_landmarks, 8, 6)
        mid_up = is_finger_up(hand_landmarks, 12, 10)
        ring_up = is_finger_up(hand_landmarks, 16, 14)
        pinky_up = is_finger_up(hand_landmarks, 20, 18)

        # Check horizontal separation between index and middle tips (avoid false positives when fingers together)
        idx_x = hand_landmarks.landmark[8].x
        mid_x = hand_landmarks.landmark[12].x
        sep = abs(idx_x - mid_x)

        # dynamic threshold: depends on hand size (distance between wrist and middle MCP)
        wrist_x = hand_landmarks.landmark[0].x
        middle_mcp_x = hand_landmarks.landmark[9].x
        hand_width_est = abs(middle_mcp_x - wrist_x) + 1e-6

        # require separation at least ~0.2 * hand_width_est (empirical)
        separated = sep > (0.18 * hand_width_est)

        return idx_up and mid_up and (not ring_up) and (not pinky_up) and separated
    except Exception:
        return False


def play_beep():
    try:
        if winsound:
            # frequency, duration
            winsound.Beep(1000, 150)
        else:
            # fallback: print
            print('\a', end='', flush=True)
    except Exception:
        print('Beep fallback')


# --- Main app ---

def main():
    os.makedirs(SAVE_DIR, exist_ok=True)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not cap.isOpened():
        print('ERROR: Could not open camera. Make sure another app is not using it.')
        return

    hands = mp_hands.Hands(model_complexity=MODEL_COMPLEXITY,
                           max_num_hands=MAX_HANDS,
                           min_detection_confidence=MIN_DETECTION_CONFIDENCE,
                           min_tracking_confidence=MIN_TRACKING_CONFIDENCE)

    gesture_active = False
    gesture_start = 0
    captured = False
    last_capture_time = 0
    frame_idx = 0

    print('Press q to quit. Show a ✌️ (peace sign) to trigger a selfie.')

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print('Failed to grab frame')
                break

            # mirror for user-friendly selfie preview
            frame = cv2.flip(frame, 1)
            display_frame = frame.copy()

            # Optional: skip frames to improve speed
            if FRAME_SKIP > 0 and (frame_idx % (FRAME_SKIP + 1)) != 0:
                frame_idx += 1
                cv2.imshow('Live - show ✌️ to take selfie', display_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                continue

            # Convert for Mediapipe
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            h, w, _ = frame.shape

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(display_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    if detect_peace_sign(hand_landmarks):
                        # avoid repeated captures: check cooldown
                        if time.time() - last_capture_time < COOLDOWN_AFTER_CAPTURE:
                            # cooldown active
                            cv2.putText(display_frame, 'Cooldown...', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,255), 2)
                        else:
                            if not gesture_active:
                                gesture_active = True
                                gesture_start = time.time()
                                captured = False

                            elapsed = time.time() - gesture_start
                            remaining = max(0, int(DELAY_SECONDS - elapsed) + 1)
                            text = f'Taking Selfie in {max(0, round(DELAY_SECONDS - elapsed,1))}s'
                            cv2.putText(display_frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
                            cv2.putText(display_frame, str(remaining), (w-120, 80), cv2.FONT_HERSHEY_DUPLEX, 3.0, (0,0,255), 6)

                            if elapsed >= DELAY_SECONDS and not captured:
                                # save selfie
                                filename = timestamp_filename('selfie', 'jpg')
                                full_path = os.path.join(SAVE_DIR, filename)
                                cv2.imwrite(full_path, frame)
                                print(f'Saved selfie to: {full_path}')

                                # apply filter
                                filtered = apply_filter(frame, mode=FILTER)
                                out_name = os.path.join(SAVE_DIR, 'filtered_' + filename)
                                cv2.imwrite(out_name, filtered)
                                print(f'Saved filtered selfie to: {out_name}')

                                # beep
                                play_beep()

                                # show filtered in a separate resizable window
                                try:
                                    cv2.namedWindow('Filtered Selfie', cv2.WINDOW_NORMAL)
                                    cv2.imshow('Filtered Selfie', filtered)
                                except Exception:
                                    pass

                                captured = True
                                gesture_active = False
                                last_capture_time = time.time()
                    else:
                        gesture_active = False
            else:
                gesture_active = False

            cv2.imshow('Live - show ✌️ to take selfie', display_frame)
            frame_idx += 1

            # quit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print('Interrupted by user')
    finally:
        hands.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
