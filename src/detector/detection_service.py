import cv2
import logging
import time
from src.detector.hand_detector import HandDetector
from src.gestures.gesture_matcher import GestureMatcher
from src.gestures.gesture_descriptor import GestureDescriptor
from src.actions.action_factory import ActionFactory

logger = logging.getLogger(__name__)

class DetectionService:
    """
    Service that captures frames from camera and runs hand detection loop.
    """
    MAX_FPS = 5  # Target frames per second
    SLEEP_SECONDS = 1 # Sleep time between gesture detections to avoid multiple triggers

    def __init__(self, camera_index=0, enable_drawing=False):
        """
        Initialize video capture and hand detector.
        """
        self.detector = HandDetector()
        self.enable_drawing = enable_drawing
        self.cap = cv2.VideoCapture(camera_index)

    def run(self):
        """
        Start detection loop.
        Press 'q' to quit.
        """
        if not self.cap.isOpened():
            logger.error("Could not open camera.")
            return

        try:
            while True:
                start_time = time.time()

                ret, frame = self.cap.read()
                if not ret:
                    logger.error("Failed to read frame from camera.")
                    break

                # Flip frame for selfie mode
                frame = cv2.flip(frame, 1)

                landmarks, label = self.detector.detect(frame)
                if landmarks:
                    logger.info(f"Detected {label} hand with {len(landmarks)} landmarks.")
                    # coords = [(lm.x, lm.y, lm.z) for lm in landmarks]
                    # logging.debug(f"Landmark coordinates: {coords}")

                    descriptor = GestureDescriptor.compute_descriptor(landmarks=landmarks, hand_label=label)
                    matched_gesture = GestureMatcher.match_gesture(current_descriptor=descriptor)

                    if matched_gesture:
                        gesture_name = matched_gesture.name
                        logger.info(f"Gesture matched: {gesture_name}")

                        action = ActionFactory.create_action(
                            action_name=matched_gesture.name,
                            action_type=matched_gesture.type,
                            action_value=matched_gesture.value
                        )

                        action.execute()

                        time.sleep(self.SLEEP_SECONDS)  # Add a small delay to avoid multiple detections in quick succession
                    else:
                        logger.info("No gesture matched.")

                    if self.enable_drawing:
                        # To draw, re-run detection to get full landmark object
                        try:
                            hand_landmarks = self.detector.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).multi_hand_landmarks[0]
                            self.detector.draw(frame, hand_landmarks)
                        except Exception as e:
                            logger.error(f"Error drawing landmarks: {e}")

                cv2.imshow('Hand Detection', frame)

                # Limit FPS
                processing_time = time.time() - start_time
                wait_time = int(max(1, (1.0 / self.MAX_FPS - processing_time) * 1000))

                if cv2.waitKey(wait_time) & 0xFF == ord('q'):
                    break
        finally:
            self.cap.release()
            cv2.destroyAllWindows()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    service = DetectionService(enable_drawing=True)
    service.run()
