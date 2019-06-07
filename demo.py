
from multiprocessing import Process
from analyst import Analyst
from videobject import VideoObject
import threading
import random
import csv
import os
import numpy as np
from threading import Thread, Lock
import time as ti
mutex = Lock()

def extract_data(path,id):
    myAnalyst = Analyst()
    for i in range(2,3):
        myAnalyst.set_sample_rate(i)
        myAnalyst.analyze(path,"people_counting")
        #print("sample_rate:",str(i)," done.")
        #print("info_amount: ",myAnalyst.memory[-1].info_amount)
        #print("resource_cost: ",myAnalyst.memory[-1].resource_cost)
    global mutex
    mutex.acquire()
    with open('dataSet_'+ id +'.csv','a') as csvfile:
        writer = csv.writer(csvfile)    
        for i in range(0,len(myAnalyst.memory)):
            obj = myAnalyst.memory[i]
            if obj.success_flag==True:
                print("---saving" + path.split('/')[-1] +"---")

                writer.writerow([
                            obj.video_name,
                            obj.sample_rate,
                            obj.info_amount['video_length'],
                            obj.analytic_result['sample_rate'],
                            obj.info_amount['target_num'],
                            obj.resource_cost['time_consumption']
                ])
    mutex.release()
        
def open_folder(path, id):
    
    f0 = os.listdir(path)
    rand = random.sample(range(0,len(f0)),40)
    for i in rand:
        if os.path.isdir(path+str(f0[i])):
            open_folder(path+str(f0[i]),id)
        else:
            t = threading.Thread(target=extract_data,args=(path+'/'+str(f0[i]),id))
            t.run()
            

if __name__ == '__main__':


    
        
    base_path = '/mnt/SmartPoleVideo/LiteOn_Videos/LiteOn_P8/LiteOn_P8_2019-05-27_00:00:00'
    """
    with open('dataSet_1.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['video_name','frames','sample_rate','targetNum','time'])
    with open('dataSet_2.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['video_name','frames','sample_rate','targetNum','time'])
    with open('dataSet_7.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['video_name','frames','sample_rate','targetNum','time'])
        """
    with open('dataSet_8.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['video_name','frames','sample_rate','targetNum','time'])
    
    """
    p1 = Process(target=extract_folder, args=(base_path + 'LiteOn_P1/','1'))
    p1.start()
    p2 = Process(target=extract_folder, args=(base_path + 'LiteOn_P2/','2'))
    p2.start()
    p3 = Process(target=extract_folder, args=(base_path + 'LiteOn_P7/','7'))
    p3.start()
    """
    p4 = Process(target=open_folder, args=(base_path,'8'))
    
    p4.start()
    
    p4.join()
    """p2.join()
    p3.join()
    p4.join()"""

    

    