import requests

# Path to your test image
image_path = "test_images/sample.jpg"

# Endpoint URL
url = "http://127.0.0.1:8000/segment/"

# Upload image
with open(image_path, "rb") as img:
    files = {"file": ("sample.jpg", img, "image/jpeg")}
    response = requests.post(url, files=files)

# Save result
if response.status_code == 200:
    with open("output_result.jpg", "wb") as f:
        f.write(response.content)
    print("✅ Result saved as output_result.jpg")
else:
    print("❌ Failed:", response.status_code, response.text)
