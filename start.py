import os
from multiprocessing import Process
from analytics.analytic_main import Analytic_Platform
from optimal_downsampling_manager.info_amount_estimator import InfoAmountEstimator

import time
listOfComponentID = []


def start_system():
    init_time = time.time()
    
    decision_process = Process(target=start_decision_manager, args=())
    analytic_process = Process(target=start_analytics_platform, args=())
    #downsample_process = Process(target=start_downsample_platform, args=(pid))
    #configure_process = Process(target=start_config_manager, args=(pid))
    
    analytic_process.start()
    decision_process.start()
    
    #downsample_process.start()
    #configure_process.start()


def start_decision_manager():
    try:
        print("running decision manager")
        IAE = InfoAmountEstimator()
        IAE.run()
    except Exception as e:
        print(e)
def start_downsample_platform():
    try:
        print("running downsample paltform")
    except Exception as e:
        print(e)
def start_config_manager():
    try:
        print("running config manager")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    start_system()
    

        