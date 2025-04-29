import cv2
import os
import json
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import folium
import webbrowser

# ---------- Global Setup ----------
image_dir = "D:\\C2A_Dataset\\Flood_Dataset\\test\\images"
label_dir = "D:\\C2A_Dataset\\Flood_Dataset\\test\\labels"

image_files = sorted([f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
if not image_files:
    raise FileNotFoundError(f"No images found in {image_dir}")

index = 0
victims_info = []  # ✅ Global variable to store detection info

image_gps_mapping = {
    "image1.png": (12.9716, 77.5946),
    "image2.png": (13.0827, 80.2707),
    "collapsed_building_image0001_3.png": (12.9716, 77.5946),
}

# ---------- Utility Functions ----------
def extract_area_name(filename):
    parts = filename.split("_")
    return parts[0] if len(parts) > 1 else "Unknown Area"

def load_image():
    global index, img_label, img_tk, victims_info
    victims_info = []  # ✅ Clear and reinitialize global list

    image_path = os.path.join(image_dir, image_files[index])
    label_path = os.path.join(label_dir, os.path.splitext(image_files[index])[0] + ".txt")

    area_name = extract_area_name(image_files[index])
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        print(f"Error: Failed to load {image_path}")
        return

    h, w, _ = image.shape
    people_count = 0

    if os.path.exists(label_path):
        with open(label_path, "r") as file:
            labels = file.readlines()

        for label in labels:
            values = label.strip().split()
            if len(values) < 5:
                continue

            class_id, x_center, y_center, box_w, box_h = map(float, values[:5])
            confidence = float(values[5]) if len(values) > 5 else 1.0

            if int(class_id) == 0:
                people_count += 1

                x1 = int((x_center - box_w / 2) * w)
                y1 = int((y_center - box_h / 2) * h)
                x2 = int((x_center + box_w / 2) * w)
                y2 = int((y_center + box_h / 2) * h)

                victims_info.append({
                    "x_center": x_center,
                    "y_center": y_center,
                    "confidence": confidence,
                    "pixel_coords": (x1, y1, x2, y2)
                })

                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        victims_info.sort(key=lambda x: x["confidence"], reverse=True)

    cv2.putText(image, f"People: {people_count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(image).resize((600, 400))
    img_tk = ImageTk.PhotoImage(img_pil)

    img_label.config(image=img_tk)
    img_label.image = img_tk
    area_label.config(text=f"Area: {area_name}")
    count_label.config(text=f"People Count: {people_count}")

def next_image():
    global index
    index = (index + 1) % len(image_files)
    load_image()

def prev_image():
    global index
    index = (index - 1) % len(image_files)
    load_image()

def plot_on_google_maps():
    global victims_info

    filename = image_files[index]

    # Try to get real GPS
    gps = image_gps_mapping.get(filename)

    if gps is None:
        # Generate dummy GPS for testing (based on index)
        base_lat, base_lon = 12.9716, 77.5946
        gps = (base_lat + index * 0.0001, base_lon + index * 0.0001)
        print(f"[Info] Using dummy GPS for {filename}: {gps}")

    lat, lon = gps

    # Create a map centered at the GPS coordinates
    m = folium.Map(location=[lat, lon], zoom_start=18)

    # Add markers for each victim
    for victim in victims_info:
        m_lat = lat + (victim['y_center'] - 0.5) * 0.0005
        m_lon = lon + (victim['x_center'] - 0.5) * 0.0005
        folium.Marker(
            location=[m_lat, m_lon],
            popup=f"Conf: {victim['confidence']:.2f}"
        ).add_to(m)

    # Save and open the map
    map_path = "victim_map.html"
    m.save(map_path)
    webbrowser.open(map_path)

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("Flood Rescue Image Viewer")
root.geometry("700x600")
root.configure(bg="black")

img_label = Label(root, bg="black")
img_label.pack(pady=10)

area_label = Label(root, text="Area: ", font=("Arial", 14, "bold"), fg="yellow", bg="black")
area_label.pack()

count_label = Label(root, text="People Count: 0", font=("Arial", 14, "bold"), fg="white", bg="black")
count_label.pack()

btn_frame = tk.Frame(root, bg="black")
btn_frame.pack(pady=10)

prev_btn = Button(btn_frame, text="⬅ Previous", font=("Arial", 12), command=prev_image)
prev_btn.grid(row=0, column=0, padx=10)

next_btn = Button(btn_frame, text="Next ➡", font=("Arial", 12), command=next_image)
next_btn.grid(row=0, column=1, padx=10)

map_btn = Button(btn_frame, text="🗺 Plot on Map", font=("Arial", 12), command=plot_on_google_maps)
map_btn.grid(row=1, column=0, columnspan=2, pady=10)

# ---------- Run ----------
load_image()
root.mainloop()
