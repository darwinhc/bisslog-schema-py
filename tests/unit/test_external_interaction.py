"""
Unit tests for the ExternalInteraction class.

This module tests the deserialization and behavior of ExternalInteraction,
including alias resolution of type_interaction to type_interaction_standard.
"""
from bisslog_schema.external_interaction import ExternalInteraction
from bisslog_schema.enums.type_external_interaction import TypeExternalInteraction


def test_from_dict_with_keyname_and_standard_type():
    """
    Test creating ExternalInteraction from dict with explicit keyname and valid type_interaction.

    Ensures type_interaction_standard is resolved correctly.
    """
    data = {
        "type_interaction": "db",
        "operation": "fetch_user_by_id",
        "description": "Access user table to fetch data"
    }
    result = ExternalInteraction.from_dict(data, keyname="user_database")
    assert result.keyname == "user_database"
    assert result.type_interaction == "db"
    assert result.operation == "fetch_user_by_id"
    assert result.description == "Access user table to fetch data"
    assert result.type_interaction_standard == TypeExternalInteraction.DATABASE


def test_from_dict_with_keyname_inside_data():
    """
    Test creating ExternalInteraction from dict where keyname is inside the dictionary.

    Ensures that the keyname from the dict is used if no explicit keyname is provided.
    """
    data = {
        "keyname": "email_sender",
        "type_interaction": "notifier",
        "operation": "send_email",
        "desc": "Call email service"
    }
    result = ExternalInteraction.from_dict(data)
    assert result.keyname == "email_sender"
    assert result.description == "Call email service"
    assert result.type_interaction_standard == TypeExternalInteraction.NOTIFIER


def test_from_dict_with_unknown_type_interaction():
    """
    Test that an unknown type_interaction results in None for the standardized field.

    This checks the fallback behavior when the alias cannot be resolved.
    """
    data = {
        "keyname": "legacy_integration",
        "type_interaction": "unknown_type",
        "operation": "legacy_call"
    }
    result = ExternalInteraction.from_dict(data)
    assert result.keyname == "legacy_integration"
    assert result.type_interaction == "unknown_type"
    assert result.type_interaction_standard is None


def test_from_dict_without_optional_fields():
    """
    Test creating ExternalInteraction with only the required field (keyname).

    Optional fields should be None by default.
    """
    data = {
        "keyname": "simple_case"
    }
    result = ExternalInteraction.from_dict(data)
    assert result.keyname == "simple_case"
    assert result.type_interaction is None
    assert result.operation is None
    assert result.description is None
    assert result.type_interaction_standard is None
