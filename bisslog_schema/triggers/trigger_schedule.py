"""Module defining trigger schedule configuration class"""
from dataclasses import dataclass
from typing import Optional, Dict, Any


from .trigger_options import TriggerOptions



@dataclass
class TriggerSchedule(TriggerOptions):
    """Options for configuring a scheduled (cron) trigger.

    Attributes
    ----------
    cronjob : str, optional
        Cron expression specifying the schedule."""
    cronjob: str
    event: Optional[Any] = None
    timezone: Optional[str] = None
    description: Optional[str] = None

    retry_policy: Optional[str] = None
    max_attempts: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TriggerSchedule":
        """Deserialize a dictionary into a TriggerSchedule instance.

        Parameters
        ----------
        data : dict
            Dictionary containing the trigger options.

        Returns
        -------
        TriggerSchedule
            An instance of a subclass implementing TriggerSchedule."""
        cronjob = data.get("cronjob")
        if not cronjob or not isinstance(cronjob, str):
            raise ValueError("The 'cronjob' field is required and must be a string.")

        event = data.get("event")

        timezone = data.get("timezone")
        if timezone is not None and not isinstance(timezone, str):
            raise ValueError("The 'timezone' field must be a string if provided.")

        description = data.get("description")
        if description is not None and not isinstance(description, str):
            raise ValueError("The 'description' field must be a string if provided.")

        retry_policy = data.get("retry_policy")
        if retry_policy is not None and not isinstance(retry_policy, str):
            raise ValueError("The 'retry_policy' field must be a string if provided.")

        max_attempts = data.get("max_attempts")
        if max_attempts is not None and (not isinstance(max_attempts, int) or max_attempts < 0):
            raise ValueError("The 'max_attempts' field must be a non-negative integer if provided.")

        return cls(
            cronjob=cronjob,
            event=event,
            timezone=timezone,
            description=description,
            retry_policy=retry_policy,
            max_attempts=max_attempts,
        )
