import cv2
import os
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk

# Paths
image_dir = "D:\\C2A_Dataset\\Flood_Dataset\\test\\images"
label_dir = "D:\\C2A_Dataset\\Flood_Dataset\\test\\labels"

# Get sorted image files
image_files = sorted([f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])

# Check if images exist
if not image_files:
    raise FileNotFoundError(f"No images found in {image_dir}")

# Initialize index
index = 0

# Function to extract area name from filename (Assumes filename format: areaName_imageXXX.png)
def extract_area_name(filename):
    parts = filename.split("_")
    if len(parts) > 1:
        return parts[0]  # Assuming first part of filename is the area name
    return "Unknown Area"

# Function to load and display image
def load_image():
    global index, img_label, img_tk

    image_path = os.path.join(image_dir, image_files[index])
    label_path = os.path.join(label_dir, image_files[index].replace('.png', '.txt').replace('.jpg', '.txt'))

    # Extract area name from filename
    area_name = extract_area_name(image_files[index])

    # Read Image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        print(f"Error: Failed to load {image_path}")
        return

    h, w, _ = image.shape

    # Read Labels
    people_count = 0
    if os.path.exists(label_path):
        with open(label_path, "r") as file:
            labels = file.readlines()

        for label in labels:
            values = label.strip().split()
            if len(values) < 5:
                continue

            class_id, x_center, y_center, box_w, box_h = map(float, values[:5])
            if int(class_id) == 0:  # Assuming '0' is the person class
                people_count += 1

            # Convert YOLO format to pixel coordinates
            x1 = int((x_center - box_w / 2) * w)
            y1 = int((y_center - box_h / 2) * h)
            x2 = int((x_center + box_w / 2) * w)
            y2 = int((y_center + box_h / 2) * h)

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display People Count on Image
    cv2.putText(image, f"People: {people_count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Convert BGR to RGB for displaying in Tkinter
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(image)
    img_pil = img_pil.resize((600, 400))  # Resize for display
    img_tk = ImageTk.PhotoImage(img_pil)

    # Update Label Widget
    img_label.config(image=img_tk)
    img_label.image = img_tk

    # Update Area Name and People Count Labels
    area_label.config(text=f"Area: {area_name}")
    count_label.config(text=f"People Count: {people_count}")

# Function to go to next image
def next_image():
    global index
    index = (index + 1) % len(image_files)
    load_image()

# Function to go to previous image
def prev_image():
    global index
    index = (index - 1) % len(image_files)
    load_image()

# Create GUI Window
root = tk.Tk()
root.title("Flood Rescue Image Viewer")
root.geometry("700x500")
root.configure(bg="black")

# Image Label
img_label = Label(root, bg="black")
img_label.pack(pady=10)

# Area Name Label
area_label = Label(root, text="Area: ", font=("Arial", 14, "bold"), fg="yellow", bg="black")
area_label.pack()

# People Count Label
count_label = Label(root, text="People Count: 0", font=("Arial", 14, "bold"), fg="white", bg="black")
count_label.pack()

# Navigation Buttons
btn_frame = tk.Frame(root, bg="black")
btn_frame.pack(pady=10)

prev_btn = Button(btn_frame, text="⬅ Previous", font=("Arial", 12), command=prev_image)
prev_btn.grid(row=0, column=0, padx=10)

next_btn = Button(btn_frame, text="Next ➡", font=("Arial", 12), command=next_image)
next_btn.grid(row=0, column=1, padx=10)

# Load first image
load_image()

# Run the GUI
root.mainloop()






