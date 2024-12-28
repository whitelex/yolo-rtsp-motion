from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, BooleanOptionalAction

# Parse command line arguments
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("--stream", type=str, help="RTSP address of video stream.")
parser.add_argument('--monitor', default=False, action=BooleanOptionalAction, help="View the live stream. If no monitor is connected then leave this disabled (no Raspberry Pi SSH sessions).")
parser.add_argument("--yolo", type=str, help="Enables YOLO object detection. Enter a comma separated list of objects you'd like the program to record. The list can be found in the coco.names file")
parser.add_argument("--model", default='yolov8n', type=str, help="Specify which model size you want to run. Default is the nano model.")
parser.add_argument("--threshold", default=350, type=int, choices=range(1,10000), help="Determines the amount of motion required to start recording. Higher values decrease sensitivity to help reduce false positives. Default 350, max 10000.")
parser.add_argument("--start_frames", default=3, type=int, choices=range(1,30), help="Number of consecutive frames with motion required to start recording. Raising this might help if there's too many false positive recordings, especially with a high frame rate stream of 60 FPS. Default 3, max 30.")
parser.add_argument("--tail_length", default=8, type=int, choices=range(1,30), help="Number of seconds without motion required to stop recording. Raise this value if recordings are stopping too early. Default 8, max 30.")
parser.add_argument("--auto_delete", default=False, action=BooleanOptionalAction, help="Enables auto-delete feature. Recordings that have total length equal to the tail_length value (seconds) are assumed to be false positives and are auto-deleted.")
parser.add_argument('--testing', default=False, action=BooleanOptionalAction, help="Testing mode disables recordings and prints out the motion value for each frame if greater than threshold. Helps fine tune the threshold value.")
parser.add_argument('--frame_click', default=False, action=BooleanOptionalAction, help="Allows user to advance frames one by one by pressing any key. For use with testing mode on video files, not live streams, so set a video file instead of an RTSP address for the --stream argument.")
parser.add_argument("--webhook", type=str, help="URL to send post notification when selected object detected.")
args = vars(parser.parse_args())

rtsp_stream = args["stream"]
monitor = args["monitor"]
thresh = args["threshold"]
start_frames = args["start_frames"]
tail_length = args["tail_length"]
auto_delete = args["auto_delete"]
testing = args["testing"]
frame_click = args["frame_click"]
webhook_url = args["webhook"]
