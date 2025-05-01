Flood Rescue Human Detection System
This project is a computer vision-based system to assist in **detecting humans in flood-affected areas** using YOLO-based annotations. It also provides a simple **Tkinter-based GUI** to navigate images, count victims, and plot them on a map using **Folium and GPS data**.

Features
-  View flood images from a directory
-  Count number of detected people using bounding boxes from YOLO labels
-  Plot victim locations on an interactive **Google Map-style HTML map** (with fake or real GPS)
-  Save detection results as `.json` automatically
-  Navigate images using "Next" and "Previous"
-  Built with Python, OpenCV, Tkinter, Folium, and Pillow

Project Structure

flood_rescue_human_detection/
│
├── import cv2.py              # Main Python GUI application
├── README.md                  # Project readme
├── victim_map.html            # Map generated dynamically (auto opens in browser)
│
├── /images/                   # Directory of input images
├── /labels/                   # YOLO-format label files (same name as image, .txt)
├── /detections_json/          # Output folder for JSON detection logs

Requirements
Install dependencies via pip:
pip install opencv-python pillow folium

How to Run

1. **Prepare directories**:
   - Store images in `images/`
   - Store YOLO `.txt` files in `labels/`

2. **Update the paths** in `import cv2.py`:

```python
image_dir = "path/to/images"
label_dir = "path/to/labels"
```

3. **(Optional)** Update GPS for each image in:

```python
image_gps_mapping = {
    "image1.png": (12.9716, 77.5946),
    ...
}
```

4. **Run the app**:

```bash
python "import cv2.py"
```

Example: Plotting on Map

- Clicking `🗺 Plot on Map` uses available GPS coordinates or dummy locations to create `victim_map.html`.
- Markers show each victim’s estimated position based on image bounding boxes.

Example JSON Output

A JSON file (e.g. `image1.json`) is saved for every detection:

```json
{
  "image": "image1.png",
  "people_count": 2,
  "victims": [
    {
      "x_center": 0.56,
      "y_center": 0.48,
      "confidence": 0.88,
      "pixel_coords": [120, 150, 200, 300]
    },
    ...
  ]
}
```
Future Improvements
- Add real-time video support
- Integrate GPS from drone or image metadata
- Add emergency alert system via Twilio/email
- Build mobile version using Kivy or Flutter

