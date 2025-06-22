import ctypes
import logging
from src.actions.base_action import BaseAction

logger = logging.getLogger(__name__)

# Windows virtual-key codes and flags
VK_VOLUME_UP = 0xAF
VK_VOLUME_DOWN = 0xAE
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
VOLUME_STEP_PRESSES   = 5  # Approx. 5 * 2% = 10%

class VolumeAction(BaseAction):
    """
    Action to adjust system volume by simulating multimedia key presses,
    so that Windows shows its native on-screen volume display (OSD).
    """

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
        if direction not in ["up", "down"]:
            logger.error(f"[VolumeAction] Invalid value '{self.value}'. Must be 'up' or 'down'")
            return

        vk = VK_VOLUME_UP if direction == "up" else VK_VOLUME_DOWN
        logger.info(f"[VolumeAction] Simulating {direction} volume key presses for gesture '{self.name}'")

        try:
            for _ in range(VOLUME_STEP_PRESSES):
                self._send_key(vk)
            logger.info(f"[VolumeAction] Volume {direction} simulated ({VOLUME_STEP_PRESSES} presses) for gesture '{self.name}'")
        except Exception as e:
            logger.error(f"[VolumeAction] Unexpected error simulating volume key: {e}", exc_info=True)



if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("=== VolumeAction Test ===\n")

    # Test volume up
    print("1. Testing volume UP")
    action_up = VolumeAction("Volume Up Gesture", "up")
    action_up.execute()
    print()
    
    # Wait 2 seconds
    import time
    time.sleep(2)
    
    # Test volume down
    print("2. Testing volume DOWN")
    action_down = VolumeAction("Volume Down Gesture", "down")
    action_down.execute()
    print()
    
    # Test invalid value
    print("3. Testing invalid value")
    action_invalid = VolumeAction("Invalid Gesture", "invalid")
    action_invalid.execute()
    print()
    
    print("=== Volume tests completed ===")
