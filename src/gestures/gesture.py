import json
from typing import Dict, List

class Gesture:
    def __init__(self,
                 name: str,
                 description: str,
                 gesture_type: str,
                 value: str | Dict,
                 descriptors: List[List[float]],
                 save: bool = True):
        
        self.name = name
        self.description = description
        self.type = gesture_type
        self.value = value
        self.descriptors = descriptors

        # If save is True, add this gesture to the gestures.json file
        if save:
            self.add_gesture()
    
    def add_gesture(self) -> None:
        gesture_data = {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "value": self.value,
            "descriptor": self.descriptor
        }

        try:
            with open("gestures.json", "r") as f:
                gestures = json.load(f)
        except FileNotFoundError:
            gestures = []

        gestures.append(gesture_data)

        with open("gestures.json", "w") as f:
            json.dump(gestures, f, indent=4)
