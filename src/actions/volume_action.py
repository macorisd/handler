import ctypes
import logging
from src.actions.base_action import BaseAction

logger = logging.getLogger(__name__)

# Windows virtual-key codes and flags
VK_VOLUME_UP = 0xAF
VK_VOLUME_DOWN = 0xAE
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002

class VolumeAction(BaseAction):
    """
    Action to adjust system volume by simulating multimedia key presses,
    so that Windows shows its native on-screen volume display (OSD).
    """

    def __init__(self, name: str, value: str, step: int = 5):
        super().__init__(name, value)
        self.step = max(1, min(50, step))  # Ensure step is between 1-50

    @staticmethod
    def _send_key(vk_code: int) -> None:
        """
        Simulate a key press and release for the given virtual-key code.
        """
        ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY, 0)
        ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)

    def execute(self) -> None:
        """
        Execute the volume adjustment by sending multimedia key events.
        """
        direction = self.value.lower()
        if direction not in ("up", "down"):
            logger.error(f"[VolumeAction] Invalid value '{self.value}'. Must be 'up' or 'down'.")
            return

        vk = VK_VOLUME_UP if direction == "up" else VK_VOLUME_DOWN
        logger.info(f"[VolumeAction] Simulating {direction} volume key presses "
                    f"({self.step} times) for gesture '{self.name}'")

        try:
            for _ in range(self.step):
                self._send_key(vk)
            logger.info(f"[VolumeAction] Volume {direction} simulated "
                        f"({self.step} presses) for gesture '{self.name}'")
        except Exception as e:
            logger.error(f"[VolumeAction] Unexpected error simulating volume key: {e}", exc_info=True)


if __name__ == "__main__":
    import time
    
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    print("=== VolumeAction Test ===\n")

    # Test volume up with default step (5 presses)
    print("1. Testing volume UP, default step")
    action_up = VolumeAction("Volume Up Gesture", "up")
    action_up.execute()
    time.sleep(2)

    # Test volume down with custom step (1 press)
    print("\n2. Testing volume DOWN, custom step of 1")
    action_down = VolumeAction("Volume Down Gesture", "down", step=1)
    action_down.execute()
    time.sleep(2)

    # Test invalid value
    print("\n3. Testing invalid value")
    action_invalid = VolumeAction("Invalid Gesture", "invalid", step=4)
    action_invalid.execute()
    print("\n=== Tests completed ===")
