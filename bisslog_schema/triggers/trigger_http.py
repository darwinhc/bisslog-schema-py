"""Module defining trigger http configuration"""
import re
from dataclasses import dataclass
from typing import Optional, Dict, Any, List, Union

from .trigger_mappable import TriggerMappable
from .trigger_options import TriggerOptions

expected_keys = ("path_query", "body", "params", "headers", "context")


@dataclass
class TriggerHttp(TriggerOptions, TriggerMappable):
    """Options for configuring an HTTP trigger.

    Attributes
    ----------
    method : str, optional
        The HTTP method (e.g., GET, POST).
    authenticator : str, optional
        The authentication mechanism associated with the trigger.
    path : str, optional
        The API route path.
    apigw : str, optional
        API Gateway identifier if applicable.
    cacheable : bool
        Indicates whether the route can be cached. Defaults to False.
    allow_cors : bool
        If True, enables CORS headers. Defaults to False.
    allowed_origins : list of str, optional
        List of allowed origins for CORS, if applicable.
    content_type : str, optional
        Expected content type for requests (e.g., application/json).
    timeout : int, optional
        Timeout for the request in milliseconds.
    rate_limit : str or int, optional
        Throttling configuration (e.g., "100r/s" or 100).
    retry_policy : str, optional
        Description or identifier for a retry policy (e.g., "exponential", "none").
    """
    method: Optional[str] = None
    authenticator: Optional[str] = None
    path: Optional[str] = None
    apigw: Optional[str] = None
    cacheable: bool = False

    allow_cors: bool = False
    allowed_origins: Optional[List[str]] = None

    content_type: Optional[str] = None

    timeout: Optional[int] = None # ms
    rate_limit: Optional[Union[str, int]] = None
    retry_policy: Optional[str] = None

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

        mapper = data.get("mapper")
        cls.verify_source_prefix(mapper, expected_keys)

        method = cls._validate_field(data.get("method"), str, "method")
        timeout = cls._validate_field(data.get("timeout"), int, "timeout", allow_none=True)
        rate_limit = cls._validate_rate_limit(data.get("rate_limit"))
        allowed_origins = cls._validate_field(
            data.get("allowed_origins"), list, "allowed_origins", allow_none=True, item_type=str
        )

        return cls(
            method=method,
            authenticator=data.get("authenticator"),
            path=data.get("path"),
            apigw=data.get("apigw"),
            cacheable=data.get("cacheable", False),
            allow_cors=data.get("allow_cors", False),
            allowed_origins=allowed_origins,
            content_type=data.get("content_type"),
            timeout=timeout,
            rate_limit=rate_limit,
            retry_policy=data.get("retry_policy"),
            mapper=mapper,
        )

    @staticmethod
    def _validate_field(value, expected_type, field_name, allow_none=False, item_type=None):
        """Validates a field's type and optional constraints."""
        if value is None:
            if allow_none:
                return value
            raise TypeError(f"The '{field_name}' field is"
                            f" required and cannot be None.")
        if not isinstance(value, expected_type):
            raise TypeError(f"The '{field_name}' field must"
                            f" be of type {expected_type.__name__}.")
        if item_type and isinstance(value, list):
            if not all(isinstance(item, item_type) for item in value):
                raise TypeError(f"All items in '{field_name}' "
                                f"must be of type {item_type.__name__}.")
        return value

    @staticmethod
    def _validate_rate_limit(rate_limit):
        """Validates the rate_limit field."""
        if rate_limit is None:
            return None
        if isinstance(rate_limit, str):
            if not re.fullmatch(r"\d+r/[sm]", rate_limit):
                raise ValueError(
                    f"Invalid rate_limit format: '{rate_limit}'. "
                    "Use formats like '100r/s' or '200r/m'."
                )
        elif not isinstance(rate_limit, int):
            raise TypeError("The 'rate_limit' field must be a string or an integer.")
        return rate_limit
