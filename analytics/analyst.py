from .pyimagesearch.centroidtracker import CentroidTracker
from .pyimagesearch.trackableobject import TrackableObject
from .videobject import VideoObject


from imutils.video import VideoStream
from imutils.video import FPS

import numpy as np
import pickle
import argparse
import imutils
import dlib
import cv2
import os

#initalize the list of class 
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]

class Analyst(object):
    def __init__(self):
        self.current_sample_rate = 0
        self.memory = []
        #self.pred_table =  pickle.load(open("dataSet/pred_table.pickle", "rb", -1))
        
        
        print("[INFO] loading model...")
        self.net=dict()
        self.net['people_counting'] = cv2.dnn.readNetFromCaffe("analytics/mobilenet_ssd/MobileNetSSD_deploy.prototxt","analytics/mobilenet_ssd/MobileNetSSD_deploy.caffemodel")

        self.currentNet = None
        self.vs = None
        self.prev_type = None
        self.write2disk =False
        
    def save_object(self,video_object):
        self.memory.append(video_object)
        return
    def save_resultvideo(self, w=False):
        self.write2disk = w
        
    def set_sample_rate(self,sample_rate):
        self.current_sample_rate = sample_rate

    def set_video_clip(self,raw_video):
        print("[INFO] opening video file...")
        self.vs = cv2.VideoCapture(raw_video)
        self.img_width = int(self.vs.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.img_height = int(self.vs.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.writer = None

    def analyze_cost(self, raw_video):
        
        predict_running_time = self.pred_table.get_pred_time(self.sample_rate)
        return predict_running_time
    
    
    def analyze(self, raw_video, frames_head, frames_tail, type):
        
        framesCounter = 0
        
        #set writer
        if self.writer is None:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.writer = cv2.VideoWriter(
                                './output/output_'+ raw_video.split('/')[-1],
                                fourcc,
                                30.0,
                                (self.img_width, self.img_height),
                                True
                            )
        self.vs.set(1,frames_head)
        fps = FPS().start()
        while True:
            
            # When analytic type changes, record the prev result, refresh the variable
            if type != self.prev_type:
                print("[INFO] refresh the analtic type")
                fps.stop()
                params = dict()
                params['output'] = './output/output_'+ raw_video.split('/')[-1]

                
                
                #reset tracker
                ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
                trackers = []
                trackableObjects = {}

                if(framesCounter>0):
                    current_obj.resource_cost['time_consumption'] = fps.elapsed()
                    current_obj.resource_cost['FPS'] = fps.fps()
                    current_obj.analytic_result['sample_rate'] = self.current_sample_rate
                    current_obj.info_amount['video_length'] = framesCounter
                    #save info_amount by type
                    if self.prev_type == 'people_counting':
                        current_obj.info_amount['target_num'] = len(trackableObjects)
                    else:
                        current_obj.info_amount['target_num'] = 0 # other type of info_amount

                    #save analytic result
                    self.save_object(current_obj)

                #create new videobject
                current_obj = VideoObject(raw_video.split('/')[-1], self.current_sample_rate)

                self.prev_type = type
                
                
            
            frame = self.vs.read()
            frame = frame[1]
            if frame is None or framesCounter > (frames_tail - frames_head):
                break
            if type == 'nothing':
                if self.write2disk:
                    self.writer.write(frame)
                framesCounter+=1
            elif type == 'people_counting':
                
                params['target'] = "person"
                params['skip_f'] = self.current_sample_rate
                params['confidence'] = 0.4
                net = self.net['people_counting']
                
                #frame = imutils.resize(frame, width=500)	
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                
                status = 'Waiting'
                rects = []
                
                if framesCounter % params['skip_f'] == 0:
                    status = 'Detecting'
                    trackers = [] 

                    blob = cv2.dnn.blobFromImage(frame, 0.007843, (self.img_width, self.img_height), 127.5)
                    net.setInput(blob)

                    detections = net.forward()
                    

                    #detection[2] is the number of object in a frame
                    for i in np.arange(0, detections.shape[2]):
                        
                        confidence = detections[0, 0, i, 2]
                        
                            
                        if confidence > params["confidence"]:
                            
                            #if object is not person, ignore it
                            idx = int(detections[0, 0, i, 1])
                            if CLASSES[idx] != params['target']:
                                continue
                            # compute the (x, y)-coordinates of the bounding box
                            # for the object
                            box = detections[0, 0, i, 3:7] * np.array([self.img_width, self.img_height, self.img_width, self.img_height])
                            (startX, startY, endX, endY) = box.astype("int")
                            
                            
                            # construct a dlib rectangle object from the bounding
                            # box coordinates and then start the dlib correlation
                            # tracker
                            tracker = dlib.correlation_tracker()
                            rect = dlib.rectangle(startX, startY, endX, endY)
                            tracker.start_track(rgb, rect)

                            # add the tracker to our list of trackers so we can
                            # utilize it during skip frames
                            trackers.append(tracker)
                            
                else:
                    # loop over the trackers
                    for tracker in trackers:
                        # set the status of our system to be 'tracking' rather
                        # than 'waiting' or 'detecting'
                        status = "Tracking"

                        # update the tracker and grab the updated position
                        tracker.update(rgb)
                        pos = tracker.get_position()

                        # unpack the position object
                        startX = int(pos.left())
                        startY = int(pos.top())
                        endX = int(pos.right())
                        endY = int(pos.bottom())

                        # add the bounding box coordinates to the rectangles list
                        rects.append((startX, startY, endX, endY))
                    
                    
                
                # use the centroid tracker to associate the (1) old object
                # centroids with (2) the newly computed object centroids
                objects = ct.update(rects)		

                # loop over the tracked objects
                for (objectID, centroid) in objects.items():
                    # check to see if a trackable object exists for the current
                    # object ID
                    to = trackableObjects.get(objectID, None)

                    # if there is no existing trackable object, create one
                    if to is None:
                        to = TrackableObject(objectID, centroid)

                    # otherwise, there is a trackable object so we can utilize it
                    # to determine direction
                    else:
                        # the difference between the y-coordinate of the *current*
                        # centroid and the mean of *previous* centroids will tell
                        # us in which direction the object is moving (negative for
                        # 'up' and positive for 'down')
                        y = [c[1] for c in to.centroids]
                        direction = centroid[1] - np.mean(y)
                        to.centroids.append(centroid)

                        # check to see if the object has been counted or not
                        if not to.counted:
                            to.counted = True

                    # store the trackable object in our dictionary
                    trackableObjects[objectID] = to
                    
                    # draw both the ID of the object and the centroid of the
                    # object on the output frame
                    
                    text = "ID {}".format(objectID)
                    cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
                    
                # frame
                info = [
                    ("Status", status),
                    ("count",len(trackableObjects))
                ]
                
                # loop over the info tuples and draw them on our frame
                for (i, (k, v)) in enumerate(info):
                    text = "{}: {}".format(k, v)
                    cv2.putText(frame, text, (10, self.img_height - ((i * 20) + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
                # check to see if we should write the frame to disk
                if self.write2disk:
                    self.writer.write(frame)

                framesCounter += 1
                fps.update()


        fps.stop()
        
        
        #self.writer.release()
        #self.vs.release()