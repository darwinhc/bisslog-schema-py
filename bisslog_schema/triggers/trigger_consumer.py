"""Module defining trigger consumer configuration class"""
from dataclasses import dataclass
from typing import Optional, Dict, Any

from .trigger_mappable import TriggerMappable
from .trigger_options import TriggerOptions
from ..enums.event_delivery_semantic import EventDeliverySemantic

expected_keys = ("event", "context")


@dataclass
class TriggerConsumer(TriggerOptions, TriggerMappable):
    """
    Options for configuring a consumer trigger (e.g., queue consumer).

    Attributes
    ----------
    queue : str, optional
        The name of the queue.
    partition : str, optional
        The partition key if applicable.
    delivery_semantic : EventDeliverySemantic
        The delivery semantic for the trigger.
    max_retries : int, optional
        Maximum number of retries.
    retry_delay : int, optional
        Delay between retries in seconds.
    dead_letter_queue : str, optional
        The name of the dead letter queue.
    batch_size : int, optional
        The size of the batch for processing messages.
    """
    queue: str = None
    partition: Optional[str] = None
    delivery_semantic: EventDeliverySemantic = EventDeliverySemantic.AT_LEAST_ONCE
    max_retries: Optional[int] = None
    retry_delay: Optional[int] = None
    dead_letter_queue: Optional[str] = None
    batch_size: Optional[int] = None

    def __post_init__(self):
        """Validates the fields after initialization."""
        self.queue = self.validate_queue(self.queue)
        self.partition = self.validate_partition(self.partition)
        self.delivery_semantic = self.validate_delivery_semantic(self.delivery_semantic)
        self.max_retries = self.validate_max_retries(self.max_retries)
        self.retry_delay = self.validate_retry_delay(self.retry_delay)
        self.dead_letter_queue = self.validate_dead_letter_queue(self.dead_letter_queue)
        self.batch_size = self.validate_batch_size(self.batch_size)

    @staticmethod
    def validate_queue(queue: Optional[str]) -> str:
        """
        Validate the `queue` field.

        Parameters
        ----------
        queue : str, optional
            The queue value to validate.

        Returns
        -------
        str
            The validated queue value.

        Raises
        ------
        ValueError
            If the queue is not a non-empty string.
        """
        if queue is None:
            raise ValueError("The 'queue' field is required and cannot be None.")
        if not isinstance(queue, str) or not queue:
            raise ValueError("The 'queue' field must be a non-empty string if provided.")
        return queue

    @staticmethod
    def validate_partition(partition: Optional[str]) -> Optional[str]:
        """
        Validate the `partition` field.

        Parameters
        ----------
        partition : str, optional
            The partition value to validate.

        Returns
        -------
        str or None
            The validated partition value.

        Raises
        ------
        ValueError
            If the partition is not a non-empty string.
        """
        if partition is not None and (not isinstance(partition, str) or not partition):
            raise ValueError("The 'partition' field must be a non-empty string if provided.")
        return partition

    @staticmethod
    def validate_delivery_semantic(
            delivery_semantic: EventDeliverySemantic) -> EventDeliverySemantic:
        """
        Validate the `delivery_semantic` field.

        Parameters
        ----------
        delivery_semantic : EventDeliverySemantic
            The delivery semantic value to validate.

        Returns
        -------
        EventDeliverySemantic
            The validated delivery semantic value.
        """
        if not isinstance(delivery_semantic, EventDeliverySemantic):
            raise ValueError("The 'delivery_semantic' field must"
                             " be of type EventDeliverySemantic.")
        return delivery_semantic

    @staticmethod
    def validate_max_retries(max_retries: Optional[int]) -> Optional[int]:
        """
        Validate the `max_retries` field.

        Parameters
        ----------
        max_retries : int, optional
            The max retries value to validate.

        Returns
        -------
        int or None
            The validated max retries value.

        Raises
        ------
        ValueError
            If the max retries is not a non-negative integer.
        """
        if max_retries is not None and (not isinstance(max_retries, int) or max_retries < 0):
            raise ValueError("The 'max_retries' field must be a non-negative integer if provided.")
        return max_retries

    @staticmethod
    def validate_retry_delay(retry_delay: Optional[int]) -> Optional[int]:
        """
        Validate the `retry_delay` field.

        Parameters
        ----------
        retry_delay : int, optional
            The retry delay value to validate.

        Returns
        -------
        int or None
            The validated retry delay value.

        Raises
        ------
        ValueError
            If the retry delay is not a non-negative integer.
        """
        if retry_delay is not None and (
                not isinstance(retry_delay, int) or retry_delay < 0):
            raise ValueError("The 'retry_delay' field must"
                             " be a non-negative integer if provided.")
        return retry_delay

    @staticmethod
    def validate_dead_letter_queue(dead_letter_queue: Optional[str]) -> Optional[str]:
        """
        Validate the `dead_letter_queue` field.

        Parameters
        ----------
        dead_letter_queue : str, optional
            The dead letter queue value to validate.

        Returns
        -------
        str or None
            The validated dead letter queue value.

        Raises
        ------
        ValueError
            If the dead letter queue is not a non-empty string.
        """
        if dead_letter_queue is not None and (
                not isinstance(dead_letter_queue, str) or not dead_letter_queue):
            raise ValueError("The 'dead_letter_queue' field must"
                             " be a non-empty string if provided.")
        return dead_letter_queue

    @staticmethod
    def validate_batch_size(batch_size: Optional[int]) -> Optional[int]:
        """
        Validate the `batch_size` field.

        Parameters
        ----------
        batch_size : int, optional
            The batch size value to validate.

        Returns
        -------
        int or None
            The validated batch size value.

        Raises
        ------
        ValueError
            If the batch size is not a non-negative integer.
        """
        if batch_size is not None and (
                not isinstance(batch_size, int) or batch_size < 0):
            raise ValueError("The 'batch_size' field must"
                             " be a non-negative integer if provided.")
        return batch_size


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
