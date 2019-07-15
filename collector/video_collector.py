#! /usr/bin/env python3
import cv2
import time
import threading
import pulsar
import numpy as np
import sys
from influxdb import InfluxDBClient

    
ERROR_MAXCOUNT = 5
URL = 'rtsp://admin:1234qwer@140.114.89.210:60226/s1'
influx_client = InfluxDBClient('localhost', 8086, 'root', 'root', 'nmsl')


# 接收攝影機串流影像，採用多執行緒的方式，降低緩衝區堆疊圖幀的問題。
class ipcamCapture:
    def __init__(self, URL):
        self.Frame = []
        self.status = False
        self.isstop = False
        self.count = 0
        self.writer = None
        # 攝影機連接。
        self.capture = cv2.VideoCapture(URL)
        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
    def start(self):
	# 把程式放進子執行緒，daemon=True 表示該執行緒會隨著主執行緒關閉而關閉。
        print('ipcam started!')
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()
        print(self.fps)

    def stop(self):
	# 記得要設計停止無限迴圈的開關。
        self.isstop = True
        print('ipcam stopped!')


    def getframe(self):
	# 當有需要影像時，再回傳最新的影像。
        return self.Frame
        
    def queryframe(self):
        while (not self.isstop):
            self.status, self.Frame = self.capture.read()
            img_height,img_width = self.Frame.shape[:2]
            
            #set writer
            if self.count % 1000 == 0:
                record_time = time.asctime(time.localtime(time.time()))
                video_name = "../dataSet/videos/webcamPole1_" + record_time +".mp4"
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                self.writer = cv2.VideoWriter(video_name, fourcc, self.fps, (img_width, img_height), True)
                self.count = 0
                print("create a new video")

                json_body = [
                {
                    "measurement": "raw_video",
                    "tags": {
                        "host": "webcamPole1",
                        "region": "nthu"
                    },
                    "time": record_time,
                    "fields": {
                        "name": "/dataSet/videos/webcamPole1" + record_time +".mp4"
                    }
                }
                ]
                influx_client.write_points(json_body)

            self.writer.write(self.Frame)
            self.count = self.count + 1
        self.capture.release()
# 連接攝影機
ipcam = ipcamCapture(URL)

# 啟動子執行緒
ipcam.start()
time.sleep(2) 
error_counter = 0

while(True):
    try:
        pass
    except Exception as e:
        print(e)
        error_counter = error_counter + 1
        if(error_counter >= ERROR_MAXCOUNT):
            ipcam = ipcamCapture(URL)
            ipcam.start()
            time.sleep(5)
            error_counter = 0
        pass
