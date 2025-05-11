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
    queue: str = None
    partition: Optional[str] = None
    delivery_semantic: EventDeliverySemantic = EventDeliverySemantic.AT_LEAST_ONCE
    max_retries: Optional[int] = None
    retry_delay: Optional[int] = None
    dead_letter_queue: Optional[str] = None
    # None means no batching, 0 means no limit, 1 means one message at a time ...
    batch_size: Optional[int] = None

    def __post_init__(self):
        """Validates the fields after initialization."""
        if self.queue is None:
            raise ValueError("The 'queue' field is required.")
        if not isinstance(self.queue, str) or not self.queue:
            raise ValueError("The 'queue' field must "
                             "be a non-empty string if provided.")

        if self.partition is not None and (
                not isinstance(self.partition, str) or not self.partition):
            raise ValueError("The 'partition' field must "
                             "be a non-empty string if provided.")
        if self.max_retries is not None and (
                not isinstance(self.max_retries, int) or self.max_retries < 0):
            raise ValueError("The 'max_retries' field must "
                             "be a non-negative integer if provided.")
        if self.retry_delay is not None and (
                not isinstance(self.retry_delay, int) or self.retry_delay < 0):
            raise ValueError("The 'retry_delay' field must "
                             "be a non-negative integer if provided.")

        if self.dead_letter_queue is not None and (
                not isinstance(self.dead_letter_queue, str) or not self.dead_letter_queue):
            raise ValueError("The 'dead_letter_queue' field must "
                             "be a non-empty string if provided.")
        if self.batch_size is not None and (
                not isinstance(self.batch_size, int) or self.batch_size < 0):
            raise ValueError("The 'batch_size' field must "
                             "be a non-negative integer if provided.")

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

        mapper: Optional[Dict[str, str]] = data.get("mapper")
        cls.verify_source_prefix(mapper, expected_keys)

        return cls(
            queue=data.get("queue"),
            partition=data.get("partition"),
            mapper=mapper,
            delivery_semantic=EventDeliverySemantic.from_value(data.get("delivery_semantic")),
            max_retries=data.get("max_retries"),
            retry_delay=data.get("retry_delay"),
            dead_letter_queue=data.get("dead_letter_queue"),
            batch_size=data.get("batch_size"),
        )
