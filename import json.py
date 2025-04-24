from ultralytics import YOLO

# Load the YOLOv8 model (use 'yolov8n.pt' for a small model, or 'yolov8m.pt' for a medium one)
model = YOLO('yolov8n.pt')

# Train the model using your dataset
model.train(
    data="D:\C2A_Dataset\Flood_Dataset\dataset.yaml", 
    imgsz=640,  # Image size (can adjust based on dataset)
    batch=4,  # Batch size (adjust based on GPU RAM)
    device='cpu'  # Use 'cpu' if you don’t have a GPU
)



