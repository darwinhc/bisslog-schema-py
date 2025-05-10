"""
This module defines a data structure for representing external interactions
in a system, such as database access or external service calls.
"""
from dataclasses import dataclass
from typing import Optional, Any, Dict

from bisslog_schema.enums.type_external_interaction import TypeExternalInteraction


@dataclass
class ExternalInteraction:
    """Represents a single external interaction, including its type, operation,
    and a standardized interaction type if resolvable.

    Attributes
    ----------
    keyname : str
        Unique key or identifier for the interaction. For example, marketing_division
    type_interaction : str, optional
        Raw string representing the type of interaction (e.g., "db", "sftp"). For example, database
    operation : str, optional
        Specific operation or action being performed. For example, get_last_sales_from_client
    type_interaction_standard : TypeExternalInteraction, optional
        Standardized type resolved from `type_interaction` using aliases."""
    keyname: str
    type_interaction: Optional[str] = None
    operation: Optional[str|list[str]] = None
    description: Optional[str] = None
    type_interaction_standard : Optional[TypeExternalInteraction] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any],
                  keyname: Optional[str] = None) -> "ExternalInteraction":
        """Deserialize a dictionary into a ExternalInteraction instance.

        Parameters
        ----------
        data : dict
            Dictionary containing the external interaction information.
        keyname : str, optional


        Returns
        -------
        ExternalInteraction
           An instance of a subclass implementing ExternalInteraction."""

        if not keyname and "keyname" not in data:
            raise ValueError("The 'keyname' field is required.")
        keyname = keyname or data["keyname"]
        if keyname and not isinstance(keyname, str):
            raise TypeError("The 'keyname' must be a string.")

        operation = data.get("operation")
        if operation and not (isinstance(operation, str) or
                              (isinstance(operation, list) and all(isinstance(op, str) for op in operation))):
            raise TypeError("The 'operation' must be a string or a list of strings.")

        type_interaction = data.get("type_interaction")
        type_interaction_standard = None
        if type_interaction is not None:
            type_interaction_standard = TypeExternalInteraction.from_str(type_interaction)


        description = data.get("description") or data.get("desc")

        return cls(
            keyname=keyname,
            type_interaction=type_interaction,
            operation=operation,
            description=description,
            type_interaction_standard=type_interaction_standard
        )
