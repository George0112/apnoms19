#encoding=utf-8
from multiprocessing.connection import Listener
from .analyst import Analyst
from optimal_downsampling_manager.decision_type import Analytic_Decision



class Analytic_Platform():
    def __init__(self):
        address = ('localhost', 6000)     
        self.listener = Listener(address)
    def run(self):
        while True:
            try:
                print("[INFO] Listening port 6000")
                conn = self.listener.accept()
                print('connection accepted from', self.listener.last_accepted)
                while True:
                    S_decision = conn.recv()
                    try:
                        print(S_decision)
                        hire_analyst(S_decision)
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
            finally:
                conn.close()
            

    def terminate_listen(self):
        self.listener.close()

def hire_analyst(S_decision):
    analyst = Analyst()
    analyst.set_sample_rate(30)
    ad = Analytic_Decision()
    for idx in range(len(S_decision)):
        if idx==0:
            analyst.set_video_clip(S_decision[0].c)
            
        else:
            if S_decision[idx].c != S_decision[idx-1].c:    
                analyst.set_video_clip(S_decision[idx].c)
        
        analyst.analyze(
                        S_decision[idx].c,
                        S_decision[idx].f[0],
                        S_decision[idx].f[1],
                        S_decision[idx].a
                    )
    print("[INFO] Analyzing end up...")

