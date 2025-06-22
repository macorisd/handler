import os
import logging
from src.actions.base_action import BaseAction

logger = logging.getLogger(__name__)

class OpenFileAction(BaseAction):
    """
    Action to open a file with the system's default application.

    The `value` parameter should be the full filesystem path to the file.
    """

    def execute(self) -> None:
        """
        Execute the open-file command.
        """
        path = self.value
        if not isinstance(path, str) or not path:
            logger.error(f"[OpenFileAction] Invalid path '{path}'. Must be a non-empty string.")
            return

        if not os.path.exists(path):
            logger.error(f"[OpenFileAction] File not found: '{path}'")
            return

        try:
            os.startfile(path)
            logger.info(f"[OpenFileAction] Opened file '{path}' for gesture '{self.name}'")
        except Exception as e:
            logger.error(f"[OpenFileAction] Failed to open file '{path}': {e}", exc_info=True)


if __name__ == "__main__":
    import time
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    print("=== OpenFileAction Test ===\n")

    # Adjust the path to a real file on your system before testing
    test_path = r"C:\\Windows\\System32\\notepad.exe"
    print(f"1. Testing open file: {test_path}")
    action = OpenFileAction("Open Notepad", test_path)
    action.execute()
    time.sleep(2)

    print("\n2. Testing invalid path")
    action_invalid = OpenFileAction("Open Invalid", r"C:\\no\\exists.txt")
    action_invalid.execute()
    print("\n=== Tests completed ===")
