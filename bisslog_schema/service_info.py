"""
Module providing the ServiceInfo dataclass to represent service-level metadata.

This module defines the ServiceInfo dataclass that extends EntityInfo to include
details such as service type, owning team, and associated use cases.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from .commands.analyze_metadata_file.metadata_analysis_report import MetadataAnalysisReport
from .entity_info import EntityInfo
from .use_case_info import UseCaseInfo


@dataclass
class ServiceInfo(EntityInfo):
    """
    Dataclass representing service metadata.

    Extends
    -------
    EntityInfo
        Base entity information with name, description, type, and tags.

    Attributes
    ----------
    service_type : Optional[str]
        The type of the service (e.g., API, batch job, etc.).
    team : Optional[str]
        The team responsible for the service.
    use_cases : Dict[str, UseCaseInfo]
        Dictionary of use cases associated with the service.
    """

    service_type: Optional[str] = None
    team: Optional[str] = None
    use_cases: Dict[str, UseCaseInfo] = field(default_factory=dict)

    @classmethod
    def analyze(cls, data: Dict[str, Any]) -> MetadataAnalysisReport:
        """
        Validate the provided data against the ServiceInfo schema.

        Parameters
        ----------
        data : dict
            The data to validate.

        Returns
        -------
        MetadataAnalysisReport
            The summary of the analysis

        Raises
        ------
        ValueError
            If validation fails.
        """
        metadata_analysis_report = super().analyze(data)
        use_cases = data.get("use_cases", {})
        validations = [
            (cls._validate_service_type, data.get("service_type")),
            (cls._validate_team, data.get("team")),
            (cls._validate_use_cases_field, use_cases)
        ]
        name = data.get("name")
        errors = []

        for func, arg in validations:
            try:
                func(arg)
            except (TypeError, ValueError) as e:
                errors.append(f"ServiceInfo'{' ' + name if name is not None else ''}'"
                              f" error: {e.args[0]}")
        metadata_analysis_report.critical_validation_count += len(validations)
        metadata_analysis_report.errors += errors

        # Validate use cases
        sub_reports = {"use_cases": []}
        if use_cases is not None:
            for key, value in use_cases.items():

                # Use case data validation
                metadata_analysis_report.critical_validation_count += 1
                if not isinstance(value, dict):
                    msg = f"Use case data for '{key}' must be a dictionary."
                    metadata_analysis_report.errors.append(msg)
                    continue

                value["keyname"] = key
                use_case_analysis_report = UseCaseInfo.analyze(value)
                sub_reports["use_cases"].append(use_case_analysis_report)
        metadata_analysis_report.sub_reports.update(sub_reports)
        return metadata_analysis_report

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ServiceInfo":
        """Create a ServiceInfo instance from a dictionary.

        This method parses a dictionary structure to create a ServiceInfo object,
        merging service-level tags with use case-specific tags.

        Parameters
        ----------
        data : dict
            A dictionary containing service information, including nested use case data.

        Returns
        -------
        ServiceInfo
            A populated ServiceInfo object.

        Raises
        ------
        ValueError
            If required fields are missing or invalid.
        """
        return cls(
            name=cls._validate_name(data.get("name")),
            description=cls._validate_description(data.get("description")),
            type=cls._validate_type(data.get("type")),
            tags=cls._validate_tags(data.get("tags", {})),
            service_type=cls._validate_service_type(data.get("service_type")),
            team=cls._validate_team(data.get("team")),
            use_cases=cls._validate_use_cases(data.get("use_cases", {})),
        )

    @classmethod
    def _validate_name(cls, name: Optional[str]) -> str:
        """Validate the `name` field.

        Parameters
        ----------
        name : Optional[str]
            The name value to validate.

        Returns
        -------
        str
            The validated name value.

        Raises
        ------
        ValueError
            If the name is not a non-empty string.
        """
        return cls._validate_required_str_field("name", name)

    @classmethod
    def _validate_service_type(cls, service_type: Optional[str]) -> Optional[str]:
        """
        Validate the `service_type` field.

        Parameters
        ----------
        service_type : Optional[str]
            The service type value to validate.

        Returns
        -------
        Optional[str]
            The validated service type value.

        Raises
        ------
        ValueError
            If the service type is not a string.
        """
        return cls._validate_optional_str_field("service_type", service_type)

    @classmethod
    def _validate_team(cls, team: Optional[str]) -> Optional[str]:
        """
        Validate the `team` field.

        Parameters
        ----------
        team : Optional[str]
            The team value to validate.

        Returns
        -------
        Optional[str]
            The validated team value.

        Raises
        ------
        ValueError
            If the team is not a string.
        """
        return cls._validate_optional_str_field("team", team)

    @staticmethod
    def _validate_use_cases_field(
            use_cases: Optional[Dict[str, Any]]) -> Optional[Dict[str, UseCaseInfo]]:
        """
        Validate the `use_cases` field.

        Parameters
        ----------
        use_cases : Optional[Dict[str, Any]]
            The use cases dictionary to validate.

        Returns
        -------
        Optional[Dict[str, UseCaseInfo]]
            The validated use cases dictionary.

        Raises
        ------
        ValueError
            If the use cases are not a dictionary or contain invalid data.
        """
        if use_cases is not None and not isinstance(use_cases, dict):
            raise ValueError("The 'use_cases' field must be a dictionary if provided.")
        return use_cases

    @classmethod
    def _validate_use_cases(cls, use_cases: Dict[str, Any]) -> Dict[str, UseCaseInfo]:
        """
        Validate the `use_cases` field and convert each use case info.

        Parameters
        ----------
        use_cases : Dict[str, Any]
            The use cases dictionary to validate.

        Returns
        -------
        Dict[str, UseCaseInfo]
            The validated use cases dictionary.

        Raises
        ------
        ValueError
            If the use cases are not a dictionary or contain invalid data.
        """
        use_cases = cls._validate_use_cases_field(use_cases)
        validated_use_cases = {}
        for key, value in use_cases.items():
            if not isinstance(value, dict):
                raise ValueError(f"Use case data for '{key}' must be a dictionary.")
            value["keyname"] = key
            try:
                validated_use_cases[key] = UseCaseInfo.from_dict(value)
            except (TypeError, ValueError) as e:
                raise ValueError(f"Error creating UseCaseInfo for '{key}': {e.args[0]}") from e
        return validated_use_cases
