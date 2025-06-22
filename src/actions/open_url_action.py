import webbrowser
import logging
from src.actions.base_action import BaseAction

logger = logging.getLogger(__name__)

class OpenURLAction(BaseAction):
    """
    Action to open a URL in the system's default web browser.

    The `value` parameter should be a string containing the full URL,
    including the scheme (e.g., "https://").
    """

    def execute(self) -> None:
        """
        Execute the open-URL command.
        """
        url = self.value
        if not isinstance(url, str) or not url:
            logger.error(f"[OpenURLAction] Invalid URL '{url}'. Must be a non-empty string.")
            return

        if not (url.startswith("http://") or url.startswith("https://")):
            logger.error(f"[OpenURLAction] URL '{url}' missing scheme (http:// or https://).")
            return

        try:
            opened = webbrowser.open(url)
            if opened:
                logger.info(f"[OpenURLAction] Opened URL '{url}' for gesture '{self.name}'")
            else:
                logger.error(f"[OpenURLAction] webbrowser.open returned False for URL '{url}'")
        except Exception as e:
            logger.error(f"[OpenURLAction] Failed to open URL '{url}': {e}", exc_info=True)


if __name__ == "__main__":
    import time
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    print("=== OpenURLAction Test ===\n")

    # Test valid URL
    test_url = "https://github.com/macorisd"
    print(f"1. Testing open URL: {test_url}")
    action = OpenURLAction("Open Example", test_url)
    action.execute()
    time.sleep(2)

    # Test missing scheme
    print("\n2. Testing URL missing scheme")
    action_no_scheme = OpenURLAction("Open No Scheme", "www.example.com")
    action_no_scheme.execute()
    time.sleep(1)

    # Test invalid value
    print("\n3. Testing invalid URL value")
    action_invalid = OpenURLAction("Open Invalid", "")
    action_invalid.execute()
    print("\n=== Tests completed ===")
