"""Module defining trigger consumer configuration class"""
from dataclasses import dataclass
from typing import Optional, Dict, Any

from .trigger_options import TriggerOptions
from ..enums.event_delivery_semantic_enum import EventDeliverySemantic


@dataclass
class TriggerConsumer(TriggerOptions):
    """Options for configuring a consumer trigger (e.g., queue consumer).

    Attributes
    ----------
    queue : str, optional
        The name of the queue.
    partition : str, optional
        The partition key if applicable."""
    queue: Optional[str] = None
    partition: Optional[str] = None
    delivery_semantic: EventDeliverySemantic = EventDeliverySemantic.AT_LEAST_ONCE

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TriggerConsumer":
        """Deserialize a dictionary into a TriggerConsumer instance.

        Parameters
        ----------
        data : dict
            Dictionary containing the trigger options.

        Returns
        -------
        TriggerConsumer
            An instance of a subclass implementing TriggerConsumer."""
        return cls(
            queue=data.get("queue"),
            partition=data.get("partition"),
            delivery_semantic=EventDeliverySemantic.from_value(data.get("delivery_semantic"))
        )
