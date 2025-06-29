import numpy as np
import math
import logging
from src.gestures.gesture_manager import GestureManager

logger = logging.getLogger(__name__)

class GestureMatcher:
    CONFIDENCE_THRESHOLD = 20.0  # Minimum confidence percentage to consider a match

    @staticmethod
    def match_gesture(current_descriptor: list[float]) -> dict | None:
        """
        Finds the best gesture match for a given descriptor from the gesture library.

        The method calculates a confidence score for each predefined gesture by comparing
        the current descriptor with the statistical model (mean and std dev) of the gesture's
        sample descriptors. It uses a Z-score and normalized Euclidean distance for this.

        Args:
            current_descriptor (list[float]): The descriptor of the currently detected gesture.

        Returns:
            dict | None: The dictionary of the best-matching gesture if its confidence
                         exceeds the threshold, otherwise None.
        """
        gesture_manager = GestureManager()  # Get the singleton instance
        best_match = None
        max_confidence = 0.0

        if not gesture_manager.gestures:
            logger.info("Gesture library is empty. No matching can be performed.")
            return None

        current_descriptor_np = np.array(current_descriptor)

        for gesture in gesture_manager.gestures:
            gesture_name = gesture.get("name", "Gesture")
            sample_descriptors = gesture.get("gesture_descriptor", [])

            if not sample_descriptors or len(sample_descriptors[0]) != len(current_descriptor):
                # logger.debug(f"Sample descriptor: {sample_descriptors[0]}")
                # logger.debug(f"Current descriptor: {current_descriptor}")

                logger.warning(f"Skipping gesture '{gesture_name}' due to incompatible descriptor format.")
                continue

            # Calculate mean and std dev for the gesture's sample descriptors
            samples_np = np.array(sample_descriptors)
            mean_descriptor = samples_np.mean(axis=0)
            std_descriptor = samples_np.std(axis=0) + 1e-6  # Add epsilon to avoid division by zero

            # Calculate confidence score
            z_scores = (current_descriptor_np - mean_descriptor) / std_descriptor
            distance = np.linalg.norm(z_scores) / math.sqrt(len(z_scores))
            confidence = (1.0 / (1.0 + distance)) * 100

            logger.info(f"Calculated confidence for gesture '{gesture_name}': {confidence:.2f}%")

            # Check if this is the best match so far
            if confidence > max_confidence:
                max_confidence = confidence
                if confidence >= GestureMatcher.CONFIDENCE_THRESHOLD:
                    best_match = gesture

        if best_match:
            logger.info(f"Best match found: '{best_match.get('name')}' with {max_confidence:.2f}% confidence.")
        else:
            logger.info(f"No gesture passed the {GestureMatcher.CONFIDENCE_THRESHOLD}% confidence threshold. Max confidence was {max_confidence:.2f}%.")

        return best_match
