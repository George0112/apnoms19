from pyimagesearch.centroidtracker import CentroidTracker
from pyimagesearch.trackableobject import TrackableObject
from pred_table import Pred_Table
from imutils.video import VideoStream
from imutils.video import FPS
from videobject import VideoObject
import numpy as np
import pickle
import argparse
import imutils
import dlib
import cv2

class Analyst(object):
    def __init__(self):
        self.current_sample_rate = 0
        self.memory = []
        self.pred_table =  pickle.load(open("dataSet/pred_table.pickle", "rb", -1))
        
    def save_object(self,video_object):
        self.memory.append(video_object)
        return
    
    def set_sample_rate(self,sample_rate):
        self.current_sample_rate = sample_rate
        
    def analyze_cost(self, raw_video):
        
        predict_running_time = self.pred_table.get_pred_time(self.sample_rate)
        return predict_running_time
    
    
    def analyze(self, raw_video, type='people_counting'):
        
        if type == 'people_counting':
            
            current_obj = VideoObject(raw_video.split('/')[-1], self.current_sample_rate)
            params = dict()
            params['prototxt'] = "mobilenet_ssd/MobileNetSSD_deploy.prototxt"
            params['model'] = "mobilenet_ssd/MobileNetSSD_deploy.caffemodel"
            params['input'] = raw_video
            params['confidence'] = 0.4
            params['output'] = 'output/output_'+ params['input'] + str(self.current_sample_rate)+'.avi'
            params['skip_f'] = self.current_sample_rate
            params['target'] = "person"

            img_width  = None   #width of frame
            img_height = None   #width of height
            writer = None
            
            #initalize the list of class 
            CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                "sofa", "train", "tvmonitor"]
            # tracker
            ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
            trackers = []
            trackableObjects = {}
           
            print("[INFO] loading model...")
            net = cv2.dnn.readNetFromCaffe(params["prototxt"], params["model"])
            
            #grab a reference to the video file
            print("[INFO] opening video file...")
            vs = cv2.VideoCapture(params["input"])
            totalFrames=0
            fps = FPS().start()
            while True:
                
                    
                frame = vs.read()
                frame = frame[1]

                if params['input'] is not None and frame is None:
                    break


                frame = imutils.resize(frame, width=500)	
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                if img_height is None or img_width is None:
                    (img_height,img_width) = frame.shape[:2]
                """
                #set writer
                if params["output"] is not None and writer is None:
                    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                    writer = cv2.VideoWriter(params["output"], fourcc, 30, (img_width, img_height), True)
                """
                status = 'Waiting'
                rects = []
                
                if totalFrames % params['skip_f'] == 0:
                    status = 'Detecting'
                    trackers = [] 

                    blob = cv2.dnn.blobFromImage(frame, 0.007843, (img_width, img_height), 127.5)
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
                            box = detections[0, 0, i, 3:7] * np.array([img_width, img_height, img_width, img_height])
                            (startX, startY, endX, endY) = box.astype("int")
                            current_obj.analytic_result['object_position'].append((totalFrames,CLASSES[idx],(startX, startY),(endX, endY)))

                            
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
                    cv2.putText(frame, text, (10, img_height - ((i * 20) + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                """
                # check to see if we should write the frame to disk
                if writer is not None:
                    writer.write(frame)"""

                totalFrames += 1
                fps.update()


            fps.stop()
            if(totalFrames>0):
                current_obj.success_flag = True
            #print("[INFO] finish analyzing...")
            #print("[INFO] total frames",totalFrames)
            if current_obj.success_flag == True:
                current_obj.resource_cost['time_consumption'] = fps.elapsed()
                current_obj.resource_cost['FPS'] = fps.fps()
                current_obj.analytic_result['sample_rate'] = self.current_sample_rate
                current_obj.info_amount['video_length'] = totalFrames
                current_obj.info_amount['target_num'] = len(trackableObjects)
                
                # calculate the score
                pred_gt = self.pred_table.get_pred_targetNum_GT(current_obj.video_name, totalFrames,self.current_sample_rate)
                if  (len(trackableObjects) == pred_gt):
                    pred_gt += 0.01
                current_obj.info_amount['score'] = 1 / abs( pred_gt - len(trackableObjects))

                #save analytic result
                self.save_object(current_obj)
            
            #writer.release()
            vs.release()