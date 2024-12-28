import cv2
import numpy as np
from datetime import datetime, timedelta
from ultralytics import YOLO
import requests
from config import args

CONFIDENCE = 0.5
font_scale = 1
thickness = 1
labels = open("coco.names").read().strip().split("\n")
colors = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")
model = YOLO(args["model"]+".pt")

yolo_list = [s.strip() for s in args["yolo"].split(",")]
last_notification_time = datetime.min

def process_yolo(img):
    results = model.predict(img, conf=CONFIDENCE, verbose=False)[0]
    object_found = False
    detected_objects = []

    for data in results.boxes.data.tolist():
        xmin, ymin, xmax, ymax, confidence, class_id = data[:6]
        class_id = int(class_id)
        if labels[class_id] in yolo_list:
            object_found = True
            detected_objects.append(labels[class_id])
        color = [int(c) for c in colors[class_id]]
        cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color=color, thickness=thickness)
        text = f"{labels[class_id]}: {confidence:.2f}"
        (text_width, text_height) = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontScale=font_scale, thickness=thickness)[0]
        text_offset_x = int(xmin)
        text_offset_y = int(ymin) - 5
        box_coords = ((text_offset_x, text_offset_y), (text_offset_x + text_width + 2, text_offset_y - text_height))
        overlay = img.copy()
        cv2.rectangle(overlay, box_coords[0], box_coords[1], color=color, thickness=cv2.FILLED)
        img = cv2.addWeighted(overlay, 0.6, img, 0.4, 0)
        cv2.putText(img, text, (int(xmin), int(ymin) - 5), cv2.FONT_HERSHEY_SIMPLEX, fontScale=font_scale, color=(0, 0, 0), thickness=thickness)

    if object_found and args["webhook"]:
        send_webhook_notification(detected_objects)

    return object_found

def send_webhook_notification(detected_objects):
    global last_notification_time
    cooldown_period = timedelta(seconds=30)

    if (datetime.now() - last_notification_time) > cooldown_period:
        try:
            response = requests.post(args["webhook"], json={"detected_objects": detected_objects})
            response.raise_for_status()
            print(f"Notification sent: {response.status_code}")
            last_notification_time = datetime.now()
        except requests.exceptions.RequestException as e:
            print(f"Failed to send notification: {e}")