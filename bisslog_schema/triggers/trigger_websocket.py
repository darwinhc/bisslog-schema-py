"""Module defining trigger websocket configuration class."""
from dataclasses import dataclass
from typing import Optional, Dict, Any

from .trigger_options import TriggerOptions


@dataclass
class TriggerWebsocket(TriggerOptions):
    """Options for configuring a WebSocket trigger.

    Attributes
    ----------
    route_key : str, optional
        The route key associated with the WebSocket connection."""
    route_key: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TriggerWebsocket":
        """Deserialize a dictionary into a TriggerWebsocket instance.

        Parameters
        ----------
        data : dict
            Dictionary containing the trigger options.

        Returns
        -------
        TriggerWebsocket
            An instance of a subclass implementing TriggerWebsocket."""
        return cls(route_key=data.get("routeKey"))
