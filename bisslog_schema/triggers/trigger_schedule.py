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
    cronjob: Optional[str] = None
    event: Optional[Any] = None

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
        return cls(cronjob=data.get("cronjob"), mapper=data.get("mapper"))
