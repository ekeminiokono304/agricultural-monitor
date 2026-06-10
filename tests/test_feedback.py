"""Verifies diagnostic feedback systems update correctly in tracking tables."""

def test_feedback_registration(client):
    """Ensures telemetric calibration coordinates stream cleanly."""
    mock_payload = {
        "scan_id": "scan_token_abc123",
        "flagged_error": True,
        "user_provided_label": "Powdery Mildew",
        "additional_context": "Visual verification verifies structural margins."
    }
    response = client.post("/feedback", json=mock_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "received"


def test_bad_feedback_payload(client):
    """Ensures input filters catch validation schema errors before processing data."""
    bad_payload = {"flagged_error": False}
    response = client.post("/feedback", json=bad_payload)
    assert response.status_code == 422