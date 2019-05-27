from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
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

         # Polynomial Coefficients
        results['coef'] = coeffs.tolist()

        # r-squared
        p = np.poly1d(coeffs)
        # fit values, and mean
        yhat = p(x)                         # or [p(z) for z in x]
        ybar = np.sum(y)/len(y)          # or sum(y)/len(y)
        ssreg = np.sum((yhat-ybar)**2)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
        sstot = np.sum((y - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
        results['r^2'] = ssreg / sstot

        return results
    def predict(self):
        print(self.polyfit(self.time_data['temporal'][0], self.time_data['temporal'][1], 1))
        fig, axes = plt.subplots(3,1, figsize=[6.4, 12])
        
        axes[0].title.set_text('temporal')
        sns.regplot(np.array(self.time_data['temporal'][0]), np.array(self.time_data['temporal'][1])
                    , ax=axes[0], color='blue', order=1, ci=None, truncate=True)
        axes[1].title.set_text('spatial')
        sns.regplot(np.array(self.time_data['spatial'][0]), np.array(self.time_data['spatial'][1])
                    , ax=axes[1], color='blue', order=1, ci=None, truncate=True)
        axes[2].title.set_text('bitrate')
        sns.regplot(np.array(self.time_data['bitrate'][0]), np.array(self.time_data['bitrate'][1])
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