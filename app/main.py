from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
import uuid
import cv2
import torch
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from PIL import Image

# Setup
IMAGEDIR = "images/"
RESULT_PATH = "images/Result.jpg"
MODEL_PATH = "furniture_detection_model.pth"

os.makedirs(IMAGEDIR, exist_ok=True)

app = FastAPI()

# Class mapping
class_names = {
    1: 'Chair',
    2: 'Sofa',
    3: 'Table'
}
class_colors = {
    1: (0, 255, 0),
    2: (0, 0, 255),
    3: (255, 0, 0)
}

def get_transform():
    return torchvision.transforms.Compose([
        torchvision.transforms.ToTensor()
    ])

def get_model_instance_segmentation(num_classes):
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model

# Load model once
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = get_model_instance_segmentation(num_classes=4)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.to(device)
model.eval()

@app.post("/segment/")
async def segment_image(file: UploadFile = File(...)):
    # Save uploaded image
    image_id = f"{uuid.uuid4()}.jpg"
    image_path = os.path.join(IMAGEDIR, image_id)
    contents = await file.read()
    with open(image_path, "wb") as f:
        f.write(contents)

    # Open and transform
    image = Image.open(image_path).convert("RGB")
    transform = get_transform()
    image_tensor = transform(image).unsqueeze(0).to(device)

    # Predict
    with torch.no_grad():
        predictions = model(image_tensor)

    boxes = predictions[0]['boxes'].cpu().numpy()
    labels = predictions[0]['labels'].cpu().numpy()
    scores = predictions[0]['scores'].cpu().numpy()

    threshold = 0.5
    filtered_indices = scores >= threshold
    boxes = boxes[filtered_indices]
    labels = labels[filtered_indices]
    scores = scores[filtered_indices]

    # Draw boxes
    image_cv = cv2.imread(image_path)
    for box, label, score in zip(boxes, labels, scores):
        xmin, ymin, xmax, ymax = [int(x) for x in box]
        color = class_colors.get(label, (255, 255, 255))
        label_text = f"{class_names.get(label, 'Unknown')} {score:.2f}"
        cv2.rectangle(image_cv, (xmin, ymin), (xmax, ymax), color, 2)
        cv2.putText(image_cv, label_text, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    # Save result image
    cv2.imwrite(RESULT_PATH, image_cv)

    return FileResponse(RESULT_PATH, media_type="image/jpeg", filename="result.jpg")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001, log_level="debug")