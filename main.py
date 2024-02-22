import cv2
import random
import time
import win32api

class webcame:

    def __init__(self):
        self.video = cv2.VideoCapture(0)
        if not self.video.isOpened():
            # Popup message
            win32api.MessageBox(0, "Video is not opened.", "Window")
            exit()

        self.record = None
        self.recording = False
        self.count = 0
        self.blink_flag = True 
        self.last_blink_time = time.time()
        self.help_flag = False
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.frame_rate = self.video.get(cv2.CAP_PROP_FPS)
        self.number = random.randint(1000,9000)

    # This code shows the information
    def note(self,frame):
        cv2.putText(frame,"Press (Q) : quit ,(R) : start/stop recording and (H) : help",(10,475),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.8,(255,0,0),1,cv2.LINE_AA)

    # This code shows the recording is started
    def start(self,frame):
        self.start_time = time.time()  # Update start time
        cv2.rectangle(frame,(5,3),(90,30),(0,0,0),-1)
        cv2.putText(frame,"Start",(10,20),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.8,(0,255,0),1,cv2.LINE_AA)
        cv2.circle(frame, (75, 17), 10, (128, 128, 128), -1)
        cv2.circle(frame, (75, 17), 6, (0, 0, 0), 1)

        if self.blink_flag:
            cv2.circle(frame, (75, 17), 4, (0, 255, 0), -1)

    # This code shows the recording is stopped
    def stop(self,frame):
        cv2.rectangle(frame,(5,3),(90,30),(0,0,0),-1)
        cv2.putText(frame,"Stop",(10,20),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.8,(0,0,255),1,cv2.LINE_AA)
        cv2.circle(frame, (70, 17), 10, (128, 128, 128), -1)
        cv2.circle(frame, (70, 17), 10, (128, 128, 128), -1)
        cv2.circle(frame, (70, 17), 6, (0, 0, 0), 1)
        cv2.circle(frame, (70, 17), 4, (0, 0, 255), -1)

    # This code shows,How to run the code and more details...
    def help(self,frame):
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        cv2.rectangle(frame,(50,50),(590,450),(60,60,60),-1)
        cv2.putText(frame,"Help:",(60,70),font,0.7,(0,255,0),1,cv2.LINE_AA)
        cv2.putText(frame,"- Press (H) to toggle help information.",(60,70 + 17*1),font,0.7,(0,255,0),1,cv2.LINE_AA)
        cv2.putText(frame,"- Press (Q) to quit the application.",(60,70 + 17*2),font,0.7,(0,255,0),1,cv2.LINE_AA)
        cv2.putText(frame,"- Press (R) to start/stop recording.",(60,70 + 17*3),font,0.7,(0,255,0),1,cv2.LINE_AA)

        cv2.putText(frame,"When recording:",(60,70 + 17*5),font,0.7,(0,255,0),1,cv2.LINE_AA)
        cv2.putText(frame,"- The word 'Start' will be displayed in green, and a ",(60,70 + 17*6),font,0.7,(0,255,0),1,cv2.LINE_AA)
        cv2.putText(frame,"   green dot will blink.",(60,70 + 17*7),font,0.7,(0,255,0),1,cv2.LINE_AA)
        cv2.putText(frame,"- Press (R) to stop recording.",(60,70 + 17*8),font,0.7,(0,255,0),1,cv2.LINE_AA)

        cv2.putText(frame,"When not recording:",(60,70 + 17*10),font,0.7,(0,255,0),1,cv2.LINE_AA)
        cv2.putText(frame,"- The word 'Stop' will be displayed in red.",(60,70 + 17*11),font,0.7,(0,255,0),1,cv2.LINE_AA)
        cv2.putText(frame,"- Press (R) to start recording.",(60,70 + 17*12),font,0.7,(0,255,0),1,cv2.LINE_AA)

        cv2.putText(frame,"License : ",(60,70 + 17*18),font,0.7,(0,255,0),1,cv2.LINE_AA)
        cv2.putText(frame,"Copyright (c) 2024 Vivek Sharma",(60,70 + 17*19),font,0.7,(0,255,0),1,cv2.LINE_AA)
        cv2.putText(frame,"GitHub Account : Vivek02Sharma",(60,70 + 17*20),font,0.7,(0,255,0),1,cv2.LINE_AA)

    def run(self):
        while(True):
            ret,frame = self.video.read()

            # here we are recording the video frame
            if self.recording:
                if self.record is None:
                    self.record = cv2.VideoWriter(f'recorded{str(self.number)}.mp4', self.fourcc, self.frame_rate, (640, 480))
                self.record.write(frame)
            else:
                if self.record is not None:
                    self.record.release()
                    self.record = None

            frame = cv2.flip(frame,1)
            self.note(frame)

            # if 'r' key is pressed then call start() else call stop()
            if self.recording:
                self.start(frame)
                self.count += 1
            else:
                if self.count > 0:
                    self.stop(frame)

            # if 'h' key is pressed then call help()
            if self.help_flag:
                self.help(frame)

            # green dot blink
            current_time = time.time()
            if current_time - self.last_blink_time >= 0.5:
                self.last_blink_time = current_time
                self.blink_flag = not self.blink_flag

            # showing the video
            cv2.imshow("Video",frame)

            key = cv2.waitKey(1)

            if key == ord('q'):
                break
            elif key == ord('r'):
                self.recording = not self.recording
            elif key == ord('h'):
                self.help_flag = not self.help_flag

        self.video.release()

        if self.record is not None:
            self.record.release()

        cv2.destroyAllWindows()

if __name__ == '__main__':
    cam = webcame()
    cam.run()

