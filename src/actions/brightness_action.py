import ctypes
import subprocess
import logging
from uuid import UUID
from src.actions.base_action import BaseAction

logger = logging.getLogger(__name__)

# Estructura GUID para ctypes
class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", ctypes.c_ulong),
        ("Data2", ctypes.c_ushort),
        ("Data3", ctypes.c_ushort),
        ("Data4", ctypes.c_ubyte * 8)
    ]

def guid_from_string(guid_str: str) -> GUID:
    """
    Converts a GUID string to a ctypes GUID structure.
    """
    u = UUID(guid_str)
    guid = GUID()
    guid.Data1 = u.time_low
    guid.Data2 = u.time_mid
    guid.Data3 = u.time_hi_version
    f = u.fields  # (time_low, time_mid, time_hi_version, clock_seq_hi_variant, clock_seq_low, node)
    guid.Data4[0] = f[3]
    guid.Data4[1] = f[4]
    node_bytes = f[5].to_bytes(6, "big")
    for i in range(6):
        guid.Data4[2 + i] = node_bytes[i]
    return guid

# Power policy GUIDs (laptop only, Windows Vista+)
VIDEO_SUBGROUP    = guid_from_string("7516b95f-f776-4464-8c53-06167f40cc99")
BRIGHTNESS_GUID   = guid_from_string("aded5e82-b909-4619-9949-f5d71dac0bcb")  # Brightness level

# Load PowrProf.dll and define prototypes
_powr = ctypes.WinDLL("PowrProf.dll")

PowerGetActiveScheme = _powr.PowerGetActiveScheme
PowerGetActiveScheme.restype  = ctypes.c_uint
PowerGetActiveScheme.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.POINTER(GUID))]

PowerWriteACValueIndex = _powr.PowerWriteACValueIndex
PowerWriteACValueIndex.restype  = ctypes.c_uint
PowerWriteACValueIndex.argtypes = [
    ctypes.c_void_p,
    ctypes.POINTER(GUID),
    ctypes.POINTER(GUID),
    ctypes.POINTER(GUID),
    ctypes.c_uint
]

PowerWriteDCValueIndex = _powr.PowerWriteDCValueIndex
PowerWriteDCValueIndex.restype  = ctypes.c_uint
PowerWriteDCValueIndex.argtypes = [
    ctypes.c_void_p,
    ctypes.POINTER(GUID),
    ctypes.POINTER(GUID),
    ctypes.POINTER(GUID),
    ctypes.c_uint
]

PowerSetActiveScheme = _powr.PowerSetActiveScheme
PowerSetActiveScheme.restype  = ctypes.c_uint
PowerSetActiveScheme.argtypes = [ctypes.c_void_p, ctypes.POINTER(GUID)]

PowerApplySettingChanges = _powr.PowerApplySettingChanges
PowerApplySettingChanges.restype  = ctypes.c_uint
PowerApplySettingChanges.argtypes = [ctypes.c_void_p, ctypes.POINTER(GUID)]


class BrightnessAction(BaseAction):
    """
    Adjusts brightness by a specified step (+1 or -1) by writing directly
    to Windows power policy to trigger native OSD.
    
    The `value` parameter should be either "up" or "down" to indicate
    the direction of brightness adjustment.
    """

    def __init__(self, name: str, value: str, step: int = 20):
        """
        Initialize the BrightnessAction.
        """
        super().__init__(name, value)
        self.step = max(1, min(100, step))  # Ensure step is between 1-100

    def execute(self) -> None:
        """
        Execute the brightness adjustment command.
        """
        direction = self.value.lower()
        if direction not in ("up", "down"):
            logger.error(f"[BrightnessAction] Invalid value '{self.value}'. Must be 'up' or 'down'")
            return

        # Get current brightness via WMI
        try:
            out = subprocess.check_output(
                ["powershell", "-Command",
                 "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness"],
                text=True
            )
            current = int(out.strip())
        except Exception as e:
            logger.error(f"[BrightnessAction] Failed reading current brightness: {e}", exc_info=True)
            return

        delta = self.step if direction == "up" else -self.step
        new_brightness = max(0, min(100, current + delta))
        logger.info(
            f"[BrightnessAction] {direction.capitalize()} from {current}% to {new_brightness}% "
            f"(step: {self.step}%) for gesture '{self.name}'"
        )

        # Get active scheme GUID
        scheme_ptr = ctypes.POINTER(GUID)()
        res = PowerGetActiveScheme(None, ctypes.byref(scheme_ptr))
        if res != 0:
            logger.error(f"[BrightnessAction] PowerGetActiveScheme failed ({res})")
            return
        scheme = scheme_ptr.contents

        # Write new value for AC and DC
        r_ac = PowerWriteACValueIndex(None, ctypes.byref(scheme),
                                      ctypes.byref(VIDEO_SUBGROUP),
                                      ctypes.byref(BRIGHTNESS_GUID),
                                      new_brightness)
        r_dc = PowerWriteDCValueIndex(None, ctypes.byref(scheme),
                                      ctypes.byref(VIDEO_SUBGROUP),
                                      ctypes.byref(BRIGHTNESS_GUID),
                                      new_brightness)
        if r_ac != 0 or r_dc != 0:
            logger.error(f"[BrightnessAction] PowerWriteValueIndex failed (AC={r_ac}, DC={r_dc})")
            return

        # Apply changes and trigger OSD
        PowerSetActiveScheme(None, ctypes.byref(scheme))
        PowerApplySettingChanges(None, ctypes.byref(scheme))

        logger.info(f"[BrightnessAction] Brightness set to {new_brightness}%.")



if __name__ == "__main__":
    import time
    
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    print("=== BrightnessAction Test ===\n")

    # Test brightness up with custom step
    print("1. Testing brightness UP (custom step = 15%)")
    action_up = BrightnessAction("Brightness Up Gesture", "up", step=15)
    action_up.execute()
    print()
    time.sleep(2)

    # Test brightness down with default step
    print("2. Testing brightness DOWN (default step = 20%)")
    action_down = BrightnessAction("Brightness Down Gesture", "down")
    action_down.execute()
    print()
    time.sleep(2)

    # Test with larger step
    print("3. Testing brightness UP with large step (50%)")
    action_large = BrightnessAction("Large Step Gesture", "up", step=30)
    action_large.execute()
    print()

    # Test invalid value
    print("4. Testing invalid value")
    action_invalid = BrightnessAction("Invalid Gesture", "invalid")
    action_invalid.execute()
    print()

    print("=== Brightness tests completed ===")
