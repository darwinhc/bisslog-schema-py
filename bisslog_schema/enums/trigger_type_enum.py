"""
Module defining the Trigger Type Enum and associated trigger classes
"""
from enum import Enum
from typing import Type

from ..triggers.trigger_consumer import TriggerConsumer
from ..triggers.trigger_options import TriggerOptions
from ..triggers.trigger_http import TriggerHttp
from ..triggers.trigger_schedule import TriggerSchedule
from ..triggers.trigger_websocket import TriggerWebsocket


class TriggerEnum(Enum):
    """Enumeration of available trigger types and their associated option classes.

    Members
    -------
    HTTP : TriggerHttp
        Represents an HTTP trigger.
    WEBSOCKET : TriggerWebsocket
        Represents a WebSocket trigger.
    CONSUMER : TriggerConsumer
        Represents a consumer or queue trigger.
    SCHEDULE : TriggerSchedule
        Represents a scheduled trigger."""
    HTTP = ("http", TriggerHttp)
    WEBSOCKET = ("websocket", TriggerWebsocket)
    CONSUMER = ("consumer", TriggerConsumer)
    SCHEDULE = ("schedule", TriggerSchedule)

    def __init__(self, value: str, cls: Type[TriggerOptions]):
        self._value_ = value  # importante: esto define el string que tendrá el enum
        self.cls = cls        # esto es tu clase asociada

    @staticmethod
    def from_str(value: str) -> "TriggerEnum":
        """Converts from string to TriggerEnum

        Parameters
        ----------
        value: str
            String value to get the member

        Returns
        -------
        TriggerEnum"""
        for trigger in TriggerEnum:
            if trigger.value == value:
                return trigger
        raise ValueError(f"Unknown trigger type: {value}")
