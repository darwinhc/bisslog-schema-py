"""Module defining trigger websocket configuration class."""
from dataclasses import dataclass
from typing import Optional, Dict, Any

from .trigger_mappable import TriggerMappable
from .trigger_options import TriggerOptions

expected_keys = ("event", "context")


@dataclass
class TriggerWebsocket(TriggerOptions, TriggerMappable):
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
        mapper: Optional[dict[str, str]] = data.get("mapper")
        cls.verify_source_prefix(mapper, expected_keys)
        return cls(route_key=data.get("routeKey"), mapper=mapper)
