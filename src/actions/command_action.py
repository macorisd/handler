import subprocess
import logging
from src.actions.base_action import BaseAction

logger = logging.getLogger(__name__)


class CommandAction(BaseAction):
    """
    Action to execute a console command in a new terminal window.

    The `value` parameter should be the full command line string to run.
    """

    def execute(self) -> None:
        """
        Execute the configured console command in a new terminal window.
        """
        logger.info(f"[CommandAction] Opening new terminal for gesture '{self.name}': {self.value}")
        try:
            cmd_command = f'start "Gesture: {self.name}" cmd /k "{self.value}"'
            
            subprocess.run(
                cmd_command,
                shell=True,
                check=True
            )
            logger.info(f"[CommandAction] New terminal opened successfully for: {self.name}")
            
        except subprocess.CalledProcessError as e:
            logger.error(
                f"[CommandAction] Error opening new terminal for command '{self.value}' "
                f"(returncode={e.returncode})",
                exc_info=True
            )
        except Exception as e:
            logger.error(
                f"[CommandAction] Unexpected error executing command '{self.value}': {str(e)}",
                exc_info=True
            )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("=== CommandAction Test ===\n")

    print("Executing command: start notepad")
    action = CommandAction("Open Notepad", "start notepad")
    action.execute()
    print()
