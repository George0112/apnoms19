from multiprocessing.connection import Client,Listener
from .decision_type import Analytic_Decision

import threading
import time

def setInterval(interval, times = -1):
    # This will be the actual decorator,
    # with fixed interval and times parameter
    def outer_wrap(function):
        # This will be the function to be
        # called
        def wrap(*args, **kwargs):
            stop = threading.Event()

            # This is another function to be executed
            # in a different thread to simulate setInterval
            def inner_wrap():
                i = 0
                while i != times and not stop.isSet():
                    stop.wait(interval)
                    function(*args, **kwargs)
                    i += 1

            t = threading.Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop
        return wrap
    return outer_wrap

class InfoAmountEstimator(object):
    def __init__(self, interval):
        self.interval = interval
        self.conn = None
    #set port, run monitor    
    def run(self):
        analy_address = ('localhost', 6000)
        
        self.conn = Client(analy_address)
        
        stopper = self.do()
        
        time.sleep(1)
        stopper.set()

    # close connection
    def close(self):
        self.conn.close()
        return

    #making analytic decision
    @setInterval(1)
    def do(self):
        #some magical algorithm
        #toy example
        ad = Analytic_Decision()
        ad.c = './dataSet/videos/LiteOn_P1_2019-07-14_13_34_43.mp4'
        ad.f = [0,100]
        ad.a = 'people_counting'

        ad2 = Analytic_Decision()
        ad2.c = './dataSet/videos/LiteOn_P1_2019-07-14_13_34_43.mp4'
        ad2.f = [101,200]
        ad2.a = 'nothing'
        S_decision=[]
        S_decision.append(ad)

        S_decision.append(ad2)
        print("[INFO] sending S_decision")
        self.conn.send(S_decision)

