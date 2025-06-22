import subprocess
import logging
from .base_action import BaseAction

logger = logging.getLogger(__name__)


class CommandAction(BaseAction):
    """
    Action to execute a shell/console command.

    The `value` parameter should be the full command line string to run.
    """

    def execute(self) -> None:
        """
        Execute the configured console command.
        """
        logger.info(f"[CommandAction] Ejecutando comando para gesto '{self.name}': {self.value}")
        try:
            # Ejecuta el comando en el shell
            result = subprocess.run(
                self.value,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            # Loguear salida estándar y de error si existiera
            if result.stdout:
                logger.debug(f"[CommandAction] STDOUT: {result.stdout.strip()}")
            if result.stderr:
                logger.warning(f"[CommandAction] STDERR: {result.stderr.strip()}")
        except subprocess.CalledProcessError as e:
            logger.error(
                f"[CommandAction] Error al ejecutar comando '{self.value}' "
                f"(returncode={e.returncode}): {e.stderr or e.stdout}",
                exc_info=True
            )
