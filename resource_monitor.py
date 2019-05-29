from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import csv

class resource_monitor:
    def __init__(self, l):
        self.time_data = {'temporal': [[0 for i in range(l)], [0 for i in range(l)]], 'spatial': [[0 for i in range(l)], [0 for i in range(l)]], 'bitrate': [[0 for i in range(l)], [0 for i in range(l)]]}
        self.size_data = {'temporal': [[0 for i in range(l)], [0 for i in range(l)]], 'spatial': [[0 for i in range(l)], [0 for i in range(l)]], 'bitrate': [[0 for i in range(l)], [0 for i in range(l)]]}
        self.truth_data = {'temporal': [[0 for i in range(l)], [0 for i in range(l)]], 'spatial': [[0 for i in range(l)], [0 for i in range(l)]], 'bitrate': [[0 for i in range(l)], [0 for i in range(l)]]}
        self.iterator = 0
        self.truth_iterator = 0
        self.l = l
    # Polynomial Regression
    def polyfit(self, x, y, degree):
        results = {}

        coeffs = np.polyfit(x, y, degree)
        return coeffs.tolist()
    
    def predict(self):
        print(self.polyfit(self.time_data['temporal'][0], self.time_data['temporal'][1], 1))
        print(self.polyfit(self.time_data['spatial'][0], self.time_data['spatial'][1], 1))
        print(self.polyfit(self.time_data['bitrate'][0], self.time_data['bitrate'][1], 1))
        
    def plot(self):
        fig, axes = plt.subplots(6,1, figsize=[6.4, 12])
        
        axes[0].title.set_text('time: temporal')
        sns.regplot(np.array(self.time_data['temporal'][0]), np.array(self.time_data['temporal'][1])
                    , ax=axes[0], color='blue', order=1, ci=None, truncate=True)
        axes[1].title.set_text('time: spatial')
        sns.regplot(np.array(self.time_data['spatial'][0]), np.array(self.time_data['spatial'][1])
                    , ax=axes[1], color='blue', order=1, ci=None, truncate=True)
        axes[2].title.set_text('time: bitrate')
        sns.regplot(np.array(self.time_data['bitrate'][0]), np.array(self.time_data['bitrate'][1])
                    , ax=axes[2], color='blue', order=1, ci=None, truncate=True)


        axes[0].title.set_text('size: temporal')
        sns.regplot(np.array(self.size_data['temporal'][0]), np.array(self.size_data['temporal'][1])
                    , ax=axes[0], color='blue', order=1, ci=None, truncate=True)
        axes[1].title.set_text('size: spatial')
        sns.regplot(np.array(self.size_data['spatial'][0]), np.array(self.size_data['spatial'][1])
                    , ax=axes[1], color='blue', order=1, ci=None, truncate=True)
        axes[2].title.set_text('size: bitrate')
        sns.regplot(np.array(self.size_data['bitrate'][0]), np.array(self.size_data['bitrate'][1])
                    , ax=axes[2], color='blue', order=1, ci=None, truncate=True)
        return 0
    def insert(self, adaption_type, par, time, size):
        self.time_data[adaption_type][0][self.iterator] = par
        self.time_data[adaption_type][1][self.iterator] = time
        self.size_data[adaption_type][0][self.iterator] = par
        self.size_data[adaption_type][1][self.iterator] = size
        self.iterator = (self.iterator+1)%self.l
    def insert_truth(self, adaption_type, par, truth):
        self.truth_data[adaption_type][0][self.truth_iterator] = par
        self.truth_data[adaption_type][1][self.truth_iterator] = truth
        self.truth_iterator = (self.truth_iterator+1) % self.l
        
    def save(self):
        lines = [
            self.time_data['temporal'][0], self.time_data['temporal'][1],
            self.time_data['spatial'][0], self.time_data['spatial'][1],
            self.time_data['bitrate'][0], self.time_data['bitrate'][1],
            self.size_data['temporal'][0], self.size_data['temporal'][1],
            self.size_data['spatial'][0], self.size_data['spatial'][1],
            self.size_data['bitrate'][0], self.size_data['bitrate'][1],
            self.truth_data['temporal'][0], self.truth_data['temporal'][1],
            self.truth_data['spatial'][0], self.truth_data['spatial'][1],
            self.truth_data['bitrate'][0], self.truth_data['bitrate'][1],
        ]
        with open('monitor.csv', 'a') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        writeFile.close()