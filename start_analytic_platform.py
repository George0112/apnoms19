import os
from multiprocessing import Process
from analytics.analytic_main import Analytic_Platform

if __name__ == '__main__':
    try:
        print("[INFO] running analytic platform")
        AP = Analytic_Platform()
        AP.run()

    except Exception as e:
        print(e)