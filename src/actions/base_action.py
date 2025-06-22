from abc import ABC, abstractmethod
import logging
from typing import Any

logger = logging.getLogger(__name__)


class BaseAction(ABC):
    """
    Abstract base class for all gesture-triggered actions.

    Subclasses must implement the `execute` method to define the action behavior.
    """

    def __init__(self, name: str, value: Any) -> None:
        """
        Initialize the action.
        """
        self.name = name
        self.value = value

    @abstractmethod
    def execute(self) -> None:
        """
        Execute the action. Must be implemented by subclasses.
        """
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, value={self.value!r})"
