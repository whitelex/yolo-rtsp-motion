# YOLO RTSP Security Camera

Modified version from [PhazerTech] https://github.com/PhazerTech/yolo-rtsp-security-cam

This project is a Python script that uses YOLO (You Only Look Once) object detection to monitor an RTSP (Real-Time Streaming Protocol) video stream. The script captures video frames, detects specified objects, and records the video when motion or specified objects are detected. It also supports sending webhook notifications and creating thumbnails for recorded videos.

## Features

- **Object Detection**: Uses YOLO to detect specified objects in the video stream.
- **Motion Detection**: Detects motion based on frame differences.
- **Recording**: Records the video stream when motion or specified objects are detected.
- **Webhook Notifications**: Sends notifications to a specified URL when objects are detected.
- **Thumbnails**: Creates thumbnails for recorded videos.
- **Metadata**: Saves metadata about recorded videos in a JSON file.
- **Auto-Delete**: Optionally deletes short recordings assumed to be false positives.
- **Health Check**: Provides an HTTP endpoint to check the application's uptime.
- **Scheduler**: Includes a PowerShell script to start the application with a specified RTSP stream and YOLO configuration.


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
    cd yolo-rtsp-motion
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
```

## Example

```bash
python main.py --stream rtsp://username:password@192.168.1.100:554/stream --yolo person,car --webhook https://example.com/webhook
```

## Command Line Arguments

- `--stream`: RTSP address of the video stream.
- `--monitor`: View the live stream. If no monitor is connected, leave this disabled.
- `--yolo`: Enables YOLO object detection. Enter a comma-separated list of objects to detect.
- `--model`: Specify which YOLO model size to use. Default is yolov8n.
- `--threshold`: Determines the amount of motion required to start recording. Default is 350.
- `--start_frames`: Number of consecutive frames with motion required to start recording. Default is 3.
- `--tail_length`: Number of seconds without motion required to stop recording. Default is 8.
- `--auto_delete`: Enables auto-delete feature for short recordings assumed to be false positives.
- `--testing`: Testing mode disables recordings and prints out the motion value for each frame.
- `--frame_click`: Allows user to advance frames one by one by pressing any key. For use with testing mode on video files.
- `--webhook`: URL to send post notification when selected object detected.

## Health Check

The application includes a health check endpoint that provides the application's uptime. The health check server listens on port 8000 and responds to requests to the `/health` endpoint.

To check the application's uptime, send an HTTP GET request to:

```bash
curl http://localhost:8000/health
```

The response will be in JSON format and include the uptime of the application.

```json
{
    "up_time": "0 days 02 hours 01 minutes"
}
```

## Scheduler

A PowerShell script (`scheduler.ps1`) is included to start the application with a specified RTSP stream and YOLO configuration. The script sets the working directory, activates the virtual environment, logs the start of the application, and starts the Python application.

To run the scheduler script, use the following command in PowerShell:

```bash
.\scheduler.ps1
```