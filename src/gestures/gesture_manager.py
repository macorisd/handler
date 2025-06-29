import json
import os
import logging

logger = logging.getLogger(__name__)

class GestureManager:
    """
    Manages loading and accessing gesture configurations from a JSON file.
    This class is implemented as a singleton to ensure that gestures are loaded only once.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GestureManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """
        Initializes the GestureManager.
        The initialization is executed only once for the singleton instance.
        """
        if self._initialized:
            return
        self.gestures = []
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.gestures_path = os.path.join(script_dir, 'gestures.json')

        self.load_gestures()
        self._initialized = True

    def load_gestures(self) -> None:
        """
        Loads gesture configurations from the JSON file into memory.
        """
        try:
            with open(self.gestures_path, 'r', encoding='utf-8') as f:
                self.gestures = json.load(f)
            logger.info(f"Successfully loaded {len(self.gestures)} gestures from '{self.gestures_path}'")
        except FileNotFoundError:
            logger.error(f"Gesture configuration file not found at '{self.gestures_path}'. No gestures were loaded.")
            self.gestures = []
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from '{self.gestures_path}': {e}", exc_info=True)
            self.gestures = []
        except Exception as e:
            logger.error(f"An unexpected error occurred while loading gestures: {e}", exc_info=True)
            self.gestures = []
