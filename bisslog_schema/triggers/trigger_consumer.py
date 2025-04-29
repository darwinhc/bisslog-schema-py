"""Module defining trigger consumer configuration class"""
from dataclasses import dataclass
from typing import Optional, Dict, Any

from .trigger_options import TriggerOptions
from ..enums.event_delivery_semantic_enum import EventDeliverySemantic


expected_keys = ("event", "context")


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

        mapper: Optional[dict[str, str]] = data.get("mapper")
        if mapper is not None:
            for source in mapper.keys():
                resource_source = source.split(".", 1)
                if resource_source not in expected_keys:
                    raise ValueError(f"Resource source {resource_source} does not exist "
                                     "for trigger consumer")

        return cls(
            queue=data.get("queue"),
            partition=data.get("partition"),
            mapper=mapper,
            delivery_semantic=EventDeliverySemantic.from_value(data.get("delivery_semantic"))
        )
