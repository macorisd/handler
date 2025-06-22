import cv2
import logging
from src.detector.hand_detector import HandDetector

class DetectionService:
    """
    Service that captures frames from camera and runs hand detection loop.
    """
    def __init__(self, camera_index=0, enable_drawing=False):
        """
        Initialize video capture and hand detector.
        """
        self.detector = HandDetector()
        self.enable_drawing = enable_drawing
        self.cap = cv2.VideoCapture(camera_index)

    def run(self):
        """
        Start detection loop. Logs landmarks when detected.
        Press 'q' to quit.
        """
        if not self.cap.isOpened():
            logging.error("Could not open camera.")
            return

        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    logging.error("Failed to read frame from camera.")
                    break

                # Flip frame for selfie mode
                frame = cv2.flip(frame, 1)

                landmarks, label = self.detector.detect(frame)
                if landmarks:
                    logging.info(f"Detected {label} hand with {len(landmarks)} landmarks.")
                    coords = [(lm.x, lm.y, lm.z) for lm in landmarks]
                    # logging.debug(f"Landmark coordinates: {coords}")
                    if self.enable_drawing:
                        # To draw, re-run detection to get full landmark object
                        try:
                            hand_landmarks = self.detector.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).multi_hand_landmarks[0]
                            self.detector.draw(frame, hand_landmarks)
                        except Exception as e:
                            logging.error(f"Error drawing landmarks: {e}", exc_info=True)

                cv2.imshow('Hand Detection', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self.cap.release()
            cv2.destroyAllWindows()


if __name__ == '__main__':
    # Configure logger to output to console
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    service = DetectionService(enable_drawing=True)
    service.run()
