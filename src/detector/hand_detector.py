import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, max_num_hands=1):
        '''
        Initialize MediaPipe Hands detector.
        '''
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def detect(self, frame):
        '''
        Detect hand landmarks in a BGR frame. Returns (landmarks, hand_label).
        '''
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        if results.multi_hand_landmarks and results.multi_handedness:
            hand_landmarks = results.multi_hand_landmarks[0]
            hand_label = results.multi_handedness[0].classification[0].label
            return hand_landmarks.landmark, hand_label
        return None, None

    def draw(self, frame, hand_landmarks):
        '''
        Draw hand landmarks on the frame.
        '''
        self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
