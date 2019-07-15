from multiprocessing.connection import Client,Listener
from decision_type import DownSample_Decision
import threading
import time


class DownsamplingDecisionMaker(object):
    def __init__(self, interval):
        self.interval = interval
        self.conn = None
    #set port, run monitor    
    def run(self):
        downsample_address = ('localhost', 8888)
        
        self.conn = Client(downsample_address)
        
        stopper = self.do('bar')
        
        time.sleep(5)
        stopper.set()

    # close connection
    def close(self):
        #self.conn.close()
        return

    #making analytic decision
    @setInterval(1)
    def do(self,name):
        #some magical algorithm
        #...
        print(name)
        #conn.send(S_decision)

IAA = DownsamplingDecisionMaker(1)
IAA.run()
