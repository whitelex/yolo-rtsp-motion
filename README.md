# YOLO RTSP Security Camera

This project is a Python script that uses YOLO (You Only Look Once) object detection to monitor an RTSP (Real-Time Streaming Protocol) video stream. The script captures video frames, detects specified objects, and records the video when motion or specified objects are detected. It also supports sending webhook notifications and creating thumbnails for recorded videos.

## Features

- **Object Detection**: Uses YOLO to detect specified objects in the video stream.
- **Motion Detection**: Detects motion based on frame differences.
- **Recording**: Records the video stream when motion or specified objects are detected.
- **Webhook Notifications**: Sends notifications to a specified URL when objects are detected.
- **Thumbnails**: Creates thumbnails for recorded videos.
- **Metadata**: Saves metadata about recorded videos in a JSON file.
- **Auto-Delete**: Optionally deletes short recordings assumed to be false positives.

## Requirements

- Python 3.6+
- OpenCV
- NumPy
- Requests
- FFmpeg
- YOLOv8
- scikit-image
- sshkeyboard

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/whitelex/yolo-rtsp-motion.git
    cd yolo-rtsp-security-cam
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script with the desired options:

```bash
python yolo-rtsp-security-cam.py --stream <RTSP_STREAM_URL> --yolo <OBJECTS_TO_DETECT> --webhook <WEBHOOK_URL>