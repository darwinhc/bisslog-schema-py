import pytest
from bisslog_schema.service_info import ServiceInfo
from bisslog_schema.use_case_info import UseCaseInfo


def test_service_info_valid_data():
    """Prueba la creación de una instancia de ServiceInfo con datos válidos."""
    data = {
        "name": "OrderService",
        "description": "Handles order processing",
        "type": "API",
        "tags": {"domain": "ecommerce"},
        "service_type": "REST",
        "team": "Order Team",
        "use_cases": {
            "create_order": {
                "name": "Create Order",
                "description": "Handles order creation",
                "tags": {"priority": "high"}
            }
        }
    }
    instance = ServiceInfo.from_dict(data)
    assert instance.name == "OrderService"
    assert instance.description == "Handles order processing"
    assert instance.type == "API"
    assert instance.tags == {"domain": "ecommerce"}
    assert instance.service_type == "REST"
    assert instance.team == "Order Team"
    assert "create_order" in instance.use_cases
    assert isinstance(instance.use_cases["create_order"], UseCaseInfo)


def test_service_info_missing_name():
    """Prueba que falte el campo 'name' lanza un ValueError."""
    data = {
        "description": "Handles order processing",
        "tags": {"domain": "ecommerce"}
    }
    with pytest.raises(ValueError, match="The 'name' field is required and must be a string."):
        ServiceInfo.from_dict(data)


def test_service_info_invalid_tags():
    """Prueba que un campo 'tags' inválido lanza un ValueError."""
    data = {
        "name": "OrderService",
        "tags": "invalid_tags"
    }
    with pytest.raises(ValueError, match="The 'tags' field must be a dictionary."):
        ServiceInfo.from_dict(data)


def test_service_info_invalid_use_cases():
    """Prueba que un campo 'use_cases' inválido lanza un ValueError."""
    data = {
        "name": "OrderService",
        "use_cases": "invalid_use_cases"
    }
    with pytest.raises(ValueError, match="The 'use_cases' field must be a dictionary."):
        ServiceInfo.from_dict(data)


def test_service_info_invalid_use_case_data():
    """Prueba que un caso de uso inválido lanza un ValueError."""
    data = {
        "name": "OrderService",
        "use_cases": {
            "create_order": "invalid_data"
        }
    }
    with pytest.raises(ValueError, match="Use case data for 'create_order' must be a dictionary."):
        ServiceInfo.from_dict(data)


def test_service_info_use_case_creation_error():
    """Prueba que un error al crear un UseCaseInfo lanza un ValueError."""
    data = {
        "name": "OrderService",
        "use_cases": {
            "create_order": {
                "name": 123  # Valor inválido para el nombre
            }
        }
    }
    with pytest.raises(ValueError, match="Error creating UseCaseInfo for 'create_order':"):
        ServiceInfo.from_dict(data)