"""
Module to define the UseCaseInfo class, which models use case metadata for a service,
including criticality, triggers, and actor details.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union

from bisslog_schema.entity_info import EntityInfo
from bisslog_schema.enums.criticality import CriticalityEnum
from bisslog_schema.external_interaction import ExternalInteraction
from bisslog_schema.triggers.trigger_info import TriggerInfo


@dataclass
class UseCaseInfo(EntityInfo):
    """
    Represents a use case with metadata including triggers, criticality, and associated actor.

    Attributes
    ----------
    triggers : List[TriggerInfo]
        A list of triggers that initiate the use case.
    criticality : Optional[Union[str, CriticalityEnum, int]]
        The criticality level of the use case. Defaults to MEDIUM.
    actor : Optional[str]
        The primary actor that interacts with the use case.
    external_interactions : List[ExternalInteraction]
        A list of external interactions associated with the use case.
    """
    triggers: List[TriggerInfo] = field(default_factory=list)
    criticality: Optional[Union[str, CriticalityEnum, int]] = CriticalityEnum.MEDIUM
    actor: Optional[str] = None
    external_interactions: List[ExternalInteraction] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict) -> "UseCaseInfo":
        """
        Creates a UseCaseInfo instance from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing use case information.

        Returns
        -------
        UseCaseInfo
            An instance populated with the provided data.

        Raises
        ------
        ValueError
            If required fields are missing or invalid.
        """
        if "name" not in data or not isinstance(data["name"], str):
            raise ValueError("The 'name' field is required and must be a string.")

        triggers_data = data.get("triggers", [])
        triggers = []
        for t in triggers_data:
            try:
                triggers.append(TriggerInfo.from_dict(t))
            except Exception as e:
                raise ValueError(f"Error processing a trigger: {e}")

        criticality = data.get("criticality", CriticalityEnum.MEDIUM)
        if isinstance(criticality, (int, float)):
            criticality = CriticalityEnum.get_from_int_val(criticality)
        elif isinstance(criticality, str) and criticality.upper() in CriticalityEnum.__members__:
            criticality = CriticalityEnum[criticality.upper()]
        elif not isinstance(criticality, CriticalityEnum):
            raise ValueError(f"Invalid criticality value: {criticality}")

        external_interactions_data = data.get("external_interactions", [])
        external_interactions = []
        if not isinstance(external_interactions_data, (list, tuple, dict)):
            raise ValueError(f"Invalid external interactions data: {external_interactions_data}")
        if isinstance(external_interactions_data, (list, tuple)):
            for ei_data in external_interactions_data:
                try:
                    external_interactions.append(ExternalInteraction.from_dict(ei_data))
                except Exception as e:
                    raise ValueError(f"Error processing an external interaction: {e}")
        elif isinstance(external_interactions_data, dict):
            for key, ei_data in external_interactions_data.items():
                try:
                    external_interactions.append(ExternalInteraction.from_dict(ei_data, keyname=key))
                except Exception as e:
                    raise ValueError(f"Error processing an external interaction with key '{key}': {e}")


        return UseCaseInfo(
            name=data["name"],
            description=data.get("description"),
            type=data.get("type"),
            tags=data.get("tags", {}),
            triggers=triggers,
            external_interactions=external_interactions,
            criticality=criticality,
            actor=data.get("actor"),
        )
