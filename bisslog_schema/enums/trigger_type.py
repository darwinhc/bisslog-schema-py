"""
Module defining the Trigger Type Enum and associated trigger classes
"""
from enum import Enum
from typing import Type, Optional

from bisslog_schema.schema_dto.triggers.trigger_consumer import TriggerConsumer
from bisslog_schema.schema_dto.triggers.trigger_options import TriggerOptions
from bisslog_schema.schema_dto.triggers import TriggerHttp
from bisslog_schema.schema_dto.triggers import TriggerSchedule
from bisslog_schema.schema_dto.triggers import TriggerWebsocket


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
        self.val = value
        self.cls = cls

    @staticmethod
    def from_str(value: str) -> Optional["TriggerEnum"]:
        """Converts from string to TriggerEnum

        Parameters
        ----------
        value: str
            String value to get the member

        Returns
        -------
        TriggerEnum"""
        for trigger in TriggerEnum:
            if trigger.val == value:
                return trigger
        return None
