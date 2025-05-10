"""
This module defines a utility class for mapping external trigger identifiers
to internal domain-specific values, typically used in configuration-based
or event-driven systems.

It also includes validation logic to ensure that mapping keys follow
expected source naming conventions.
"""
from dataclasses import dataclass
from typing import Optional, Dict, Iterable


@dataclass
class TriggerMappable:
    """A class that represents a mapping from external trigger values to internal values.

    This can be used in configuration-driven architectures where triggers
    (e.g., event names or message types) from external sources need to be
    translated or normalized into internal values used in the domain logic.

    Attributes
    ----------
    mapper : dict of str to str, optional
        A dictionary mapping external trigger values (keys) to internal representations (values).
        If None, no mapping will be applied."""
    mapper: Optional[Dict[str, str]] = None

    @staticmethod
    def verify_source_prefix(mapper: Optional[dict[str, str]], expected_keys: Iterable[str]):
        """
        Validates that all keys in the provided mapper start with a prefix that is allowed.

        Parameters
        ----------
        mapper : dict of str to str, optional
            The mapping of source paths to values. Keys must start with one of
            the expected prefixes.
        expected_keys : Iterable of str
            A list or set of valid prefixes that the keys in `mapper` are expected to start with.

        Raises
        ------
        ValueError
            If any key in the mapper does not start with a valid prefix from `expected_keys`.
        """
        if mapper is not None:
            for source_path in mapper:
                source_prefix = source_path.split(".", 1)[0]
                if source_prefix not in expected_keys:
                    raise ValueError(
                        f"Invalid source path '{source_path}': unknown prefix '{source_prefix}'. "
                        f"Expected one of: {sorted(expected_keys)}."
                    )
