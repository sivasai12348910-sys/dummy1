import pytest

@pytest.mark.django_db
def test_image_upload(client):
    url = "/upload_image/?device_id=1&reading_id=abc123"

    image_bytes = b"fake-image-data"

    response = client.post(
        url,
        data=image_bytes,
        content_type="image/jpeg"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "image stored"


@pytest.mark.django_db
def test_image_upload_missing_params(client):
    response = client.post(
        "/upload_image/",
        data=b"img",
        content_type="image/jpeg"
    )

    assert response.status_code == 400