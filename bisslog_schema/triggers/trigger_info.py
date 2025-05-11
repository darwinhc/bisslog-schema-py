"""Module defining trigger conceptual information class"""
from dataclasses import dataclass
from typing import Dict, Any, Union

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
    options: Union[TriggerOptions, Dict[str, Any]]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "TriggerInfo":
        """
        Creates a TriggerInfo instance from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing the trigger configuration.

        Returns
        -------
        TriggerInfo
            An instance of TriggerInfo.

        Raises
        ------
        ValueError
            If required fields are missing or invalid.
        """
        # Validate and parse the trigger type
        type_str = data.get("type", "http")
        if not type_str:
            raise ValueError("Trigger 'type' is required and cannot be None or empty.")

        trigger_type = TriggerEnum.from_str(type_str)

        # Validate and parse the options
        options = data.get("options", {})

        if not isinstance(options, (dict, TriggerOptions)):
            raise TypeError("The 'options' field must be a dictionary "
                            "or an instance of TriggerOptions.")

        if trigger_type is not None and trigger_type.cls and isinstance(options, dict):
            try:
                options = trigger_type.cls.from_dict(options)
            except Exception as e:
                raise ValueError("Error parsing options for trigger"
                                 f" type '{trigger_type}': {e}") from e

        return TriggerInfo(type=trigger_type, options=options)
