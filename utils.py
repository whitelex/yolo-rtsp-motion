import os
import sys
import time
from datetime import datetime
import cv2
from sshkeyboard import listen_keyboard  # Import listen_keyboard

class suppress_stdout_stderr(object):
    def __enter__(self):
        self.outnull_file = open(os.devnull, 'w')
        self.errnull_file = open(os.devnull, 'w')
        self.old_stdout_fileno_undup    = sys.stdout.fileno()
        self.old_stderr_fileno_undup    = sys.stderr.fileno()
        self.old_stdout_fileno = os.dup ( sys.stdout.fileno() )
        self.old_stderr_fileno = os.dup ( sys.stderr.fileno() )
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        os.dup2 ( self.outnull_file.fileno(), self.old_stdout_fileno_undup )
        os.dup2 ( self.errnull_file.fileno(), self.old_stderr_fileno_undup )
        sys.stdout = self.outnull_file
        sys.stderr = self.errnull_file
        return self
    def __exit__(self, *_):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        os.dup2 ( self.old_stdout_fileno, self.old_stdout_fileno_undup )
        os.dup2 ( self.old_stderr_fileno, self.old_stderr_fileno_undup )
        os.close ( self.old_stdout_fileno )
        os.close ( self.old_stderr_fileno )
        self.outnull_file.close()
        self.errnull_file.close()

def receive_frames(cap, q, loop, rtsp_stream, recording, stop_ffmpeg):
    if cap.isOpened():
        ret, frame = cap.read()
        while loop:
            ret, frame = cap.read()
            if ret:
                q.put(frame)
            else:
                if recording: stop_ffmpeg()
                now_time = datetime.now().strftime('%H-%M-%S')
                print(now_time + " Camera disconnected. Attempting to reconnect.")
                while loop:
                    with suppress_stdout_stderr():
                        cap = cv2.VideoCapture(rtsp_stream)
                    if cap.isOpened():
                        now_time = datetime.now().strftime('%H-%M-%S')
                        print(now_time + " Camera successfully reconnected.")
                        break
                    else: time.sleep(5)

def press(key, loop):
    if key == 'q':
        loop[0] = False

def input_keyboard(on_press):
    listen_keyboard(
        on_press=on_press,
    )

def timer(loop):
    delay = False
    period = 2
    now = datetime.now()
    now_time = now.time()
    start1 = now_time.replace(hour=0, minute=0, second=0, microsecond=0)
    start2 = now_time.replace(hour=0, minute=0, second=2, microsecond=10000)
    start_t=time.time()
    while loop[0]:
        now = datetime.now()
        now_time = now.time()
        if(now_time>=start1 and now_time<=start2):
            day_num = now.weekday()
            if day_num == 0: print("Monday "+now.strftime('%m-%d-%Y'))
            elif day_num == 1: print("Tuesday "+now.strftime('%m-%d-%Y'))
            elif day_num == 2: print("Wednesday "+now.strftime('%m-%d-%Y'))
            elif day_num == 3: print("Thursday "+now.strftime('%m-%d-%Y'))
            elif day_num == 4: print("Friday "+now.strftime('%m-%d-%Y'))
            elif day_num == 5: print("Saturday "+now.strftime('%m-%d-%Y'))
            elif day_num == 6: print("Sunday "+now.strftime('%m-%d-%Y'))
            delay = True
        time.sleep(period - ((time.time() - start_t) % period))
        if delay:
            delay = False
            time.sleep(period - ((time.time() - start_t) % period))