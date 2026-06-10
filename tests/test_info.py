"""Verifies tracking logic endpoints, core health structures, and data indexes."""

def test_health_endpoint_contract(client):
    """Verifies critical operational state indicators on the server."""
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"
    assert json_data["model_loaded"] is True


def test_model_info_validation_array(client):
    """Ensures structural description mappings are accurate and up-to-date."""
    response = client.get("/model/info")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["architecture"] == "EfficientNetB0"
    assert "Healthy" in json_data["classes"]


def test_disease_catalog_distribution(client):
    """Validates target processing capacity distributions."""
    response = client.get("/diseases")
    assert response.status_code == 200
    assert response.json()["supported_count"] == 5