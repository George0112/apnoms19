import os
from multiprocessing import Process
from optimal_downsampling_manager.info_amount_estimator import InfoAmountEstimator

import time

if __name__ == '__main__':
    try:
        print("[INFO] Running decision platform")
        IAA = InfoAmountEstimator(1)
        IAA.run()

    except Exception as e:
        print(e)