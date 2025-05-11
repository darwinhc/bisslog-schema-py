"""Module defining trigger schedule configuration class"""
from dataclasses import dataclass
from typing import Optional, Dict, Any

try:
    from zoneinfo import available_timezones
    _ZONE_INFO_AVAILABLE = True
except ImportError:
    try:
        from backports.zoneinfo import available_timezones
        _ZONE_INFO_AVAILABLE = True
    except ImportError:
        available_timezones = None
        _ZONE_INFO_AVAILABLE = False

from .trigger_options import TriggerOptions



@dataclass
class TriggerSchedule(TriggerOptions):
    """
    Options for configuring a scheduled (cron) trigger.

    Attributes
    ----------
    cronjob : str
        Cron expression specifying the schedule.
    event : Any, optional
        Event data associated with the trigger.
    timezone : str, optional
        Timezone for the schedule.
    description : str, optional
        Description of the trigger.
    retry_policy : str, optional
        Retry policy for the trigger.
    max_attempts : int, optional
        Maximum number of retry attempts.
    """
    cronjob: str
    event: Optional[Any] = None
    timezone: Optional[str] = None
    description: Optional[str] = None
    retry_policy: Optional[str] = None
    max_attempts: Optional[int] = None

    @classmethod
    def validate_cronjob(cls, cronjob: Any) -> str:
        """
        Validate the `cronjob` field.

        Parameters
        ----------
        cronjob : Any
            The cronjob value to validate.

        Returns
        -------
        str
            The validated cronjob value.

        Raises
        ------
        ValueError
            If the cronjob is not a valid string.
        """
        if not cronjob or not isinstance(cronjob, str):
            raise ValueError("The 'cronjob' field is required and must be a string.")
        return cronjob

    @classmethod
    def validate_timezone(cls, timezone: Any) -> str:
        """
        Validate the `timezone` field.

        Parameters
        ----------
        timezone : Any
            The timezone value to validate.

        Returns
        -------
        str
            The validated timezone value.

        Raises
        ------
        ValueError
            If the timezone is not a valid string or not recognized.
        """
        if timezone is not None:
            if not isinstance(timezone, str):
                raise ValueError("The 'timezone' field must be a string if provided.")
            cls.validate_tz_on_standard(timezone)
        return timezone

    @classmethod
    def validate_tz_on_standard(cls, timezone: str) -> str:
        """
        Check if the timezone is valid.

        Parameters
        ----------
        timezone : str
            The timezone value to validate.

        Returns
        -------
        str
            The validated timezone value.

        Raises
        ------
        ValueError
            If the timezone is not recognized.
        """
        if _ZONE_INFO_AVAILABLE:
            if timezone not in available_timezones():
                raise ValueError(f"Invalid timezone string: {timezone}")
        return timezone

    @classmethod
    def validate_description(cls, description: Any) -> Any:
        """
        Validate the `description` field.

        Parameters
        ----------
        description : Any
            The description value to validate.

        Returns
        -------
        Any
            The validated description value.

        Raises
        ------
        ValueError
            If the description is not a valid string.
        """
        if description is not None and not isinstance(description, str):
            raise ValueError("The 'description' field must be a string if provided.")
        return description

    @classmethod
    def validate_retry_policy(cls, retry_policy: Any) -> Any:
        """
        Validate the `retry_policy` field.

        Parameters
        ----------
        retry_policy : Any
            The retry policy value to validate.

        Returns
        -------
        Any
            The validated retry policy value.

        Raises
        ------
        ValueError
            If the retry policy is not a valid string.
        """
        if retry_policy is not None and not isinstance(retry_policy, str):
            raise ValueError("The 'retry_policy' field must be a string if provided.")
        return retry_policy

    @classmethod
    def validate_max_attempts(cls, max_attempts: Any) -> Any:
        """
        Validate the `max_attempts` field.

        Parameters
        ----------
        max_attempts : Any
            The max attempts value to validate.

        Returns
        -------
        Any
            The validated max attempts value.

        Raises
        ------
        ValueError
            If the max attempts is not a non-negative integer.
        """
        if max_attempts is not None and (not isinstance(max_attempts, int) or max_attempts < 0):
            raise ValueError("The 'max_attempts' field must be a non-negative integer if provided.")
        return max_attempts

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TriggerSchedule":
        """
        Deserialize a dictionary into a TriggerSchedule instance.

        Parameters
        ----------
        data : dict
            Dictionary containing the trigger options.

        Returns
        -------
        TriggerSchedule
            An instance of TriggerSchedule.

        Raises
        ------
        ValueError
            If any field fails validation.
        """
        cronjob = cls.validate_cronjob(data.get("cronjob"))
        timezone = cls.validate_timezone(data.get("timezone"))
        description = cls.validate_description(data.get("description"))
        retry_policy = cls.validate_retry_policy(data.get("retry_policy"))
        max_attempts = cls.validate_max_attempts(data.get("max_attempts"))

        return cls(
            cronjob=cronjob,
            event=data.get("event"),
            timezone=timezone,
            description=description,
            retry_policy=retry_policy,
            max_attempts=max_attempts,
        )
