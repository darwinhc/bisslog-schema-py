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

    @classmethod
    def from_dict(cls, data: dict) -> "UseCaseInfo":
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

        triggers = cls._parse_triggers(data.get("triggers", []))
        criticality = cls._parse_criticality(data.get("criticality", CriticalityEnum.MEDIUM))
        external_interactions = cls._parse_external_interactions(
            data.get("external_interactions", [])
        )

        return cls(
            name=data["name"],
            description=data.get("description"),
            type=data.get("type"),
            tags=data.get("tags", {}),
            triggers=triggers,
            external_interactions=external_interactions,
            criticality=criticality,
            actor=data.get("actor"),
        )

    @staticmethod
    def _parse_triggers(triggers_data: list) -> List[TriggerInfo]:
        """Parses and validates the triggers data."""
        triggers = []
        for t in triggers_data:
            try:
                triggers.append(TriggerInfo.from_dict(t))
            except Exception as e:
                raise ValueError(f"Error processing a trigger: {e}") from e
        return triggers

    @staticmethod
    def _parse_criticality(criticality: Union[str, int, CriticalityEnum]) -> CriticalityEnum:
        """Parses and validates the criticality value."""
        if isinstance(criticality, (int, float)):
            return CriticalityEnum.get_from_int_val(criticality)
        if isinstance(criticality, str) and criticality.upper() in CriticalityEnum.__members__:
            return CriticalityEnum[criticality.upper()]
        if isinstance(criticality, CriticalityEnum):
            return criticality
        raise ValueError(f"Invalid criticality value: {criticality}")

    @staticmethod
    def _parse_external_interactions(
            external_interactions_data: Union[list, dict]
    ) -> List[ExternalInteraction]:
        """Parses and validates the external interaction data."""
        if not isinstance(external_interactions_data, (list, tuple, dict)):
            raise ValueError(f"Invalid external interactions data: {external_interactions_data}")

        external_interactions = []
        if isinstance(external_interactions_data, (list, tuple)):
            for ei_data in external_interactions_data:
                try:
                    external_interactions.append(ExternalInteraction.from_dict(ei_data))
                except Exception as e:
                    raise ValueError(f"Error processing an external interaction: {e}") from e
        elif isinstance(external_interactions_data, dict):
            for key, ei_data in external_interactions_data.items():
                try:
                    external_interactions.append(
                        ExternalInteraction.from_dict(ei_data, keyname=key)
                    )
                except Exception as e:
                    raise ValueError(
                        f"Error processing an external interaction with key '{key}': {e}"
                    ) from e
        return external_interactions
