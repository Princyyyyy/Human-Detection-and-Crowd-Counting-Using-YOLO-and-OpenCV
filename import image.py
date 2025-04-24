import os

image_folder = "D:/C2A_Dataset/Flood_Dataset/test/images"
allowed_extensions = {".jpg", ".jpeg", ".png"}

for file in os.listdir(image_folder):
    if not any(file.lower().endswith(ext) for ext in allowed_extensions):
        print(f"⚠️ Unexpected file format: {file}")
