import os

dataset_path = "D:/C2A_Dataset/Flood_Dataset/test/images"

if os.path.exists(dataset_path):
    print(f"✅ Dataset folder found: {dataset_path}")
    print("📂 Files in the directory:", os.listdir(dataset_path))
else:
    print(f"❌ Dataset folder NOT found: {dataset_path}")
