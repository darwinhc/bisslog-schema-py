"""Module defining trigger conceptual information class"""
from dataclasses import dataclass
from typing import Dict, Any

from ..enums.trigger_type import TriggerEnum
from .trigger_options import TriggerOptions


@dataclass
class TriggerInfo:
    """Represents a complete trigger configuration including its type and specific options.

    Attributes
    ----------
    type : TriggerEnum
        The type of the trigger (e.g., HTTP, WebSocket).
    options : TriggerOptions
        The configuration options specific to the trigger type."""
    type: TriggerEnum
    options: TriggerOptions|Dict[str, Any]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "TriggerInfo":
        """Enumeration of available trigger types and their associated option classes.

        Parameters
        ----------
        data : dict
            Dictionary containing the trigger options.
        Returns
        -------
        TriggerInfo
            An instance of a subclass implementing TriggerSchedule."""

        type_str = data.get("type", "http")
        if not type_str:
            raise ValueError("Trigger 'type' is required")

        trigger_type = TriggerEnum.from_str(type_str)

        options = data.get("options", {})
        if trigger_type is not None:
            cls = trigger_type.cls
            options = cls.from_dict(options)

        return TriggerInfo(trigger_type, options)
