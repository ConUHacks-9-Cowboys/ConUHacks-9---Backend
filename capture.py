import cv2
import numpy as np
import mediapipe as mp
import math

IMPORTANT_INDEXES = [
    70,
    63,
    105,
    66,
    107,
    46,
    53,
    52,
    65,
    55,
    336,
    296,
    334,
    293,
    300,
    285,
    295,
    282,
    283,
    276,
    146,
    91,
    181,
    84,
    17,
    314,
    405,
    321,
    375,
    185,
    40,
    39,
    37,
    0,
    267,
    269,
    270,
    409,
]

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5
)


# Color rolling function
def get_rolling_color(t):
    r = int((math.sin(t) + 1) * 127)  # Red intensity varies
    g = int((math.sin(t + 2) + 1) * 127)  # Green intensity varies
    b = int((math.sin(t + 4) + 1) * 127)  # Blue intensity varies
    return (r, g, b)


def start_capture(shared_dict):
    t = 0
    # Capture webcam feed
    # list available cameras with their names
    for i in range(0, 10):
        try:
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f"Camera {i}: {cap.getBackendName()}")
                cap.release()
        except:
            pass

    cap = cv2.VideoCapture(3)
    cap.set(cv2.CAP_PROP_AUTO_WB, 1)
    cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 4500)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)

    while cap.isOpened():
        ret, frame = cap.read()
        original_frame = frame.copy()
        frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if not ret:
            break

        # Convert frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect face landmarks
        results = face_mesh.process(frame_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Extract key facial points (e.g., eyebrows, eyes, mouth)
                landmarks = np.array([(lm.x, lm.y) for lm in face_landmarks.landmark])
                landmarks *= (frame_width, frame_height)

                for point in landmarks:
                    frame = cv2.circle(frame, point.astype(int), 1, (255, 0, 0), -1)

                for index in IMPORTANT_INDEXES:
                    frame = cv2.circle(
                        frame, landmarks[index].astype(int), 3, get_rolling_color(t), -1
                    )

        # Show video feed
        cv2.imshow("Micro-Expression Stress Detection", frame)

        if shared_dict["request"] == 1:
            shared_dict["request"] = 0
            shared_dict["frame"] = original_frame

        t += 0.01

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
