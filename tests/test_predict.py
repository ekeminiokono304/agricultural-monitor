"""Validates the execution correctness of the prediction pipelines."""

def test_disease_prediction_pipeline(client, sample_image_bytes):
    """Tests an end-to-end multi-part payload evaluation call loop."""
    payload_files = {
        'file': ('test_leaf.jpg', sample_image_bytes, 'image/jpeg')
    }
    payload_data = {
        'field_id': 'NGA-AKWA-IBOM-ZONE-MOCK'
    }
    response = client.post("/predict/disease", files=payload_files, data=payload_data)
    assert response.status_code == 200
    json_payload = response.json()
    assert json_payload["status"] == "success"
    assert "detected_disease" in json_payload
    assert "agent_reasoning_output" in json_payload


def test_missing_payload_file_handling(client):
    """Verifies error catching protocols during bad requests."""
    payload_data = {'field_id': 'MISSING-FILE-FIELD'}
    response = client.post("/predict/disease", data=payload_data)
    assert response.status_code == 422


def test_batch_prediction_pipeline(client, sample_image_bytes):
    """Verifies simultaneous execution flows across batch tracking queues."""
    payload_files = [
        ('files', ('leaf_1.jpg', sample_image_bytes, 'image/jpeg')),
        ('files', ('leaf_2.jpg', sample_image_bytes, 'image/jpeg'))
    ]
    payload_data = {'field_id': 'BATCH-ZONE-A'}
    response = client.post("/predict/batch", files=payload_files, data=payload_data)
    assert response.status_code == 200
    assert response.json()["total"] == 2