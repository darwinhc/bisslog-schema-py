"""Module defining trigger configuration abstract class"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class TriggerOptions(ABC):
    """Abstract base class for trigger-specific options.

    All trigger option classes must implement the from_dict method for deserialization."""

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TriggerOptions":
        """Deserialize a dictionary into a TriggerOptions instance.

        Parameters
        ----------
        data : dict
            Dictionary containing the trigger options.

        Returns
        -------
        TriggerOptions
            An instance of a subclass implementing TriggerOptions."""
        raise NotImplementedError("from_dict not implemented")
