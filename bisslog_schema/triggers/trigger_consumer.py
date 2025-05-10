"""Module defining trigger consumer configuration class"""
from dataclasses import dataclass
from typing import Optional, Dict, Any

from .trigger_mappable import TriggerMappable
from .trigger_options import TriggerOptions
from ..enums.event_delivery_semantic import EventDeliverySemantic


expected_keys = ("event", "context")


@dataclass
class TriggerConsumer(TriggerOptions, TriggerMappable):
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

        mapper: Optional[dict[str, str]] = data.get("mapper")
        cls.verify_source_prefix(mapper, expected_keys)

        return cls(
            queue=data.get("queue"),
            partition=data.get("partition"),
            mapper=mapper,
            delivery_semantic=EventDeliverySemantic.from_value(data.get("delivery_semantic"))
        )
