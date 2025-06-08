import os
import requests

def test_segment_api():
    url = "http://127.0.0.1:8000/segment/"
    test_image = "test_images/sample.jpg"

    assert os.path.exists(test_image), "Test image not found!"

    with open(test_image, "rb") as img:
        files = {"file": ("sample.jpg", img, "image/jpeg")}
        response = requests.post(url, files=files)

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"

    with open("test_images/test_result.jpg", "wb") as f:
        f.write(response.content)

def test_segment_api_invalid_file_type():
    url = "http://127.0.0.1:8000/segment/"
    files = {"file": ("test.txt", b"This is not an image", "text/plain")}
    response = requests.post(url, files=files)

    assert response.status_code in (400, 422)  # Expected failure

def test_segment_api_no_file():
    url = "http://127.0.0.1:8000/segment/"
    response = requests.post(url, files={})  # No file provided

    assert response.status_code == 422  # Unprocessable Entity (validation error)
