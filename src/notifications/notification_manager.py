import logging
from win10toast import ToastNotifier

logger = logging.getLogger(__name__)

class NotificationManager:
    """
    Manager for sending Windows toast notifications.

    Uses the win10toast library to display native Windows 10+ notifications.
    """

    def __init__(self):
        """
        Initialize the notification manager.

        Args:
            default_duration (int): Default display time for notifications in seconds.
        """
        self._toaster = ToastNotifier()

    def send(self, title: str, message: str, duration: int = 4, icon_path: str = None, threaded: bool = True) -> bool:
        """
        Send a Windows toast notification.

        Args:
            title (str): Title text of the notification.
            message (str): Body text of the notification.
            duration (int, optional): How long to display the notification, in seconds.
            icon_path (str, optional): Path to a .ico file for the notification icon.
            threaded (bool): Whether to show the notification in a non-blocking thread.

        Returns:
            bool: True if the notification was successfully queued, False otherwise.
        """
        try:
            result = self._toaster.show_toast(
                title,
                message,
                icon_path=icon_path,
                duration=duration,
                threaded=threaded
            )
            logger.info(f"[NotificationManager] Notification queued: title='{title}', message='{message}'")
            return result
        except Exception as e:
            logger.error(f"[NotificationManager] Failed to send notification: {e}", exc_info=True)
            return False


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    notifier = NotificationManager()
    success = notifier.send("Gesture Detected", "Volume increased successfully")
    if success:
        logger.info("Example notification sent successfully.")
    else:
        logger.error("Example notification failed to send.")
