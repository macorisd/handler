from typing import Dict

from src.actions.base_action import BaseAction
from src.actions.volume_action import VolumeAction
from src.actions.brightness_action import BrightnessAction
from src.actions.open_file_action import OpenFileAction
from src.actions.command_action import CommandAction
from src.actions.open_url_action import OpenURLAction


class ActionFactory:
    @staticmethod
    def create_action(action_name: str, action_type: str, action_value: str | Dict) -> BaseAction:
        if action_type == "volume":
            return VolumeAction(name=action_name, value=action_value.get("command"), step=action_value.get("step"))
        if action_type == "brightness":
            return BrightnessAction(name=action_name, value=action_value.get("command"), step=action_value.get("step"))
        if action_type == "file":
            return OpenFileAction(name=action_name, value=action_value)
        if action_type == "command":
            return CommandAction(name=action_name, value=action_value)
        if action_type == "url":
            return OpenURLAction(name=action_name, value=action_value)

        raise ValueError(f"Unknown action type: {action_type}")