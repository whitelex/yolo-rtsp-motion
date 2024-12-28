import time
import os
import sys
import cv2
import queue
import threading
import numpy as np
from datetime import datetime
from skimage.metrics import mean_squared_error as ssim
from sshkeyboard import listen_keyboard, stop_listening
from config import args, rtsp_stream, monitor, thresh, start_frames, tail_length, auto_delete, testing, frame_click, webhook_url
from detection import process_yolo, send_webhook_notification
from ffmpeg_utils import start_ffmpeg, stop_ffmpeg, create_thumbnail
from metadata import save_metadata
from utils import suppress_stdout_stderr, receive_frames, press, input_keyboard, timer

# Initialize variables
loop = [True]  # Use a list to allow modification within functions
cap = cv2.VideoCapture(rtsp_stream)
fps = cap.get(cv2.CAP_PROP_FPS)
period = 1/fps
tail_length = tail_length*fps
recording = False
ffmpeg_copy = 0
activity_count = 0
yolo_count = 0
ret, img = cap.read()
if img.shape[1]/img.shape[0] > 1.55:
    res = (256,144)
else:
    res = (216,162)
blank = np.zeros((res[1],res[0]), np.uint8)
resized_frame = cv2.resize(img, res)
gray_frame = cv2.cvtColor(resized_frame,cv2.COLOR_BGR2GRAY)
old_frame = cv2.GaussianBlur(gray_frame, (5,5), 0)
if monitor:
    cv2.namedWindow(rtsp_stream, cv2.WINDOW_NORMAL)

q = queue.Queue()

# Start the background threads
receive_thread = threading.Thread(target=receive_frames, args=(cap, q, loop, rtsp_stream, recording, stop_ffmpeg))
receive_thread.start()
keyboard_thread = threading.Thread(target=input_keyboard, args=(lambda key: press(key, loop),))
keyboard_thread.start()
timer_thread = threading.Thread(target=timer, args=(loop,))
timer_thread.start()

# Inform user that the system is ready
print("System is ready and in standby mode, capturing movements... Press 'Q' to exit.")

# Main loop
while loop[0]:
    if q.empty() != True:
        img = q.get()

        # Resize image, make it grayscale, then blur it
        resized_frame = cv2.resize(img, res)
        gray_frame = cv2.cvtColor(resized_frame,cv2.COLOR_BGR2GRAY)
        final_frame = cv2.GaussianBlur(gray_frame, (5,5), 0)

        # Calculate difference between current and previous frame, then get ssim value
        diff = cv2.absdiff(final_frame, old_frame)
        result = cv2.threshold(diff, 5, 255, cv2.THRESH_BINARY)[1]
        ssim_val = int(ssim(result,blank))
        old_frame = final_frame

        # Print value for testing mode
        if testing and ssim_val > thresh:
            print("motion: "+ str(ssim_val))

        # Count the number of frames where the ssim value exceeds the threshold value.
        # If the number of these frames exceeds start_frames value, run YOLO detection.
        # Start recording if an object from the user provided list is detected
        if not recording:
            if ssim_val > thresh:
                activity_count += 1
                if activity_count >= start_frames:
                    if process_yolo(img):
                        yolo_count += 1
                    else:
                        yolo_count = 0
                    if yolo_count > 1:
                        filedate = datetime.now().strftime('%H-%M-%S')
                        if not testing:
                            base_path = os.path.abspath(os.path.join(os.getcwd(), "..", "home-security", "public", "feed"))
                            folderdate = os.path.join(base_path, datetime.now().strftime('%Y-%m-%d'))
                            if not os.path.isdir(folderdate):
                                os.makedirs(folderdate)
                            filename = os.path.join(folderdate, f'{filedate}.mkv')
                            ffmpeg_copy = start_ffmpeg(rtsp_stream, filename)
                            print(filedate + " recording started")
                        else:
                            print(filedate + " recording started - Testing mode")
                        recording = True
                        activity_count = 0
                        yolo_count = 0
            else:
                activity_count = 0
                yolo_count = 0

        # If already recording, count the number of frames where there's no motion activity
        # or no object detected and stop recording if it exceeds the tail_length value
        else:
            if not process_yolo(img) or ssim_val < thresh:
                activity_count += 1
                if activity_count >= tail_length:
                    filedate = datetime.now().strftime('%H-%M-%S')
                    if not testing:
                        stop_ffmpeg(ffmpeg_copy)
                        print(filedate + " recording stopped")
                        # If auto_delete argument was provided, delete recording if total
                        # length is equal to the tail_length value, indicating a false positive
                        if auto_delete:
                            recorded_file = cv2.VideoCapture(filename)
                            recorded_frames = recorded_file.get(cv2.CAP_PROP_FRAME_COUNT)
                            if recorded_frames < tail_length + (fps/2) and os.path.isfile(filename):
                                os.remove(filename)
                                print(filename + " was auto-deleted")
                        else:
                            create_thumbnail(filename)
                            save_metadata(filename, folderdate)
                    else:
                        print(filedate + " recording stopped - Testing mode")
                    recording = False
                    activity_count = 0
            else:
                activity_count = 0

        # Monitor the stream
        if monitor:
            cv2.imshow(rtsp_stream, img)
            if frame_click:
                cv_key = cv2.waitKey(0) & 0xFF
                if cv_key == ord("q"):
                    loop[0] = False
                if cv_key == ord("n"):
                    continue
            else:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    loop[0] = False
    else:
        time.sleep(period/2)

# Gracefully end threads and exit
stop_listening()
if ffmpeg_copy:
    stop_ffmpeg(ffmpeg_copy)
receive_thread.join()
keyboard_thread.join()
timer_thread.join()
cv2.destroyAllWindows()
print("Exiting")