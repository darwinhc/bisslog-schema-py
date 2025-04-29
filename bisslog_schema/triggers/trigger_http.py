"""Module defining trigger http configuration"""
from dataclasses import dataclass
from typing import Optional, Dict, Any

from .trigger_options import TriggerOptions


@dataclass
class TriggerHttp(TriggerOptions):
    """Options for configuring an HTTP trigger.

    Attributes
    ----------
    method : str, optional
        The HTTP method (e.g., GET, POST).
    authenticator : str, optional
        The authentication mechanism associated with the trigger.
    route : str, optional
        The API route path.
    apigw : str, optional
        API Gateway identifier if applicable.
    cacheable : bool
        Indicates whether the route can be cached. Defaults to False."""
    method: Optional[str] = None
    authenticator: Optional[str] = None
    route: Optional[str] = None
    apigw: Optional[str] = None
    cacheable: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TriggerHttp":
        """Deserialize a dictionary into a TriggerWebsocket instance.

        Parameters
        ----------
        data : dict
            Dictionary containing the trigger options.

        Returns
        -------
        TriggerHttp
            An instance of a subclass implementing TriggerWebsocket."""
        return cls(
            method=data.get("method"),
            authenticator=data.get("authenticator"),
            route=data.get("route"),
            apigw=data.get("apigw"),
            cacheable=data.get("cacheable", False)
        )
