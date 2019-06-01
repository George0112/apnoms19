from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import csv
import pandas as pd
from scipy.optimize import curve_fit

class resource_monitor:
    def __init__(self, l):
        self.time_data = {'temporal': [[0 for i in range(l)], [0 for i in range(l)]], 'spatial': [[0 for i in range(l)], [0 for i in range(l)]], 'bitrate': [[0 for i in range(l)], [0 for i in range(l)]]}
        self.size_data = {'temporal': [[0 for i in range(l)], [0 for i in range(l)]], 'spatial': [[0 for i in range(l)], [0 for i in range(l)]], 'bitrate': [[0 for i in range(l)], [0 for i in range(l)]]}
        self.truth_data = {'temporal': [[0 for i in range(l)], [0 for i in range(l)]], 'spatial': [[0 for i in range(l)], [0 for i in range(l)]], 'bitrate': [[0 for i in range(l)], [0 for i in range(l)]]}
        self.iterator_temporal = 0
        self.iterator_spatial = 0
        self.iterator_bitrate = 0
        self.truth_iterator_temporal = 0
        self.truth_iterator_spatial = 0
        self.truth_iterator_bitrate = 0
        self.l = l
    # Polynomial Regression
    def polyfit(self, x, y, degree):
        results = {}

        coeffs = np.polyfit(x, y, degree)
        return coeffs.tolist()
    
    def predict(self, adaption_type, data='time'):
        df = pd.read_csv(data+adaption_type+'.csv', header=None)
        print(self.polyfit(df[0], df[1], 2))
        return 0
            
    def plot(self, adaption_type, data='time'):
        df = pd.read_csv(data+adaption_type+'.csv', header=None)
        fig, axes = plt.subplots(1,1)

        axes.title.set_text(adaption_type)
        axes.set_xlabel('fps' if adaption_type=='temporal' else 'resolution' if adaption_type=='spatial' else 'bitrate')
        axes.set_ylabel('second' if data=='time' else 'size')
        sns.regplot(df[0], df[1]
                    , ax=axes, color='blue', order=2, ci=None, truncate=True)
        return 0
    
    def plot_exp(self, adaption_type, data='time'):
        df = pd.read_csv(data+adaption_type+'.csv', header=None)
        # plot data
        plt.scatter(df[0].values,df[1].values, label="data")

        # Fitting
        model = lambda x, offset, A:  offset+A*np.exp((x))
        popt, pcov = curve_fit(model, df[0].values, 
                                  df[1].values)
        #plot fit
        x = np.linspace(df[0].values.min(),df[0].values.max(),250)
        plt.plot(x,model(x,*popt), label="fit")

        plt.xlim(None,df[0].values.max())
        plt.legend()
        plt.show()
    
    def insert(self, adaption_type, par, time, size):
        if adaption_type == 'temporal':
            iterator = self.iterator_temporal
            self.iterator_temporal = (self.iterator_temporal+1)%self.l
        elif adaption_type == 'spatial':
            iterator = self.iterator_spatial
            self.iterator_spatial = (self.iterator_spatial+1)%self.l
        else:
            iterator = self.iterator_bitrate
            self.iterator_bitrate = (self.iterator_bitrate+1)%self.l
            
        self.time_data[adaption_type][0][iterator] = par
        self.time_data[adaption_type][1][iterator] = time
        self.size_data[adaption_type][0][iterator] = par
        self.size_data[adaption_type][1][iterator] = size
        if iterator+1 == self.l:
            self.save('time_'+adaption_type)
            self.save('size_'+adaption_type)
        
    def insert_truth(self, adaption_type, par, truth):
        if adaption_type == 'temporal':
            iterator = self.truth_iterator_temporal
            self.truth_iterator_temporal = (self.truth_iterator_temporal+1)%self.l
        elif adaption_type == 'spatial':
            itrator = self.truth_iterator_spatial
            self.truth_iterator_spatial = (self.truth_iterator_spatial+1)%self.l
        else:
            iterator = self.truth_iterator_bitrate
            self.truth_iterator_biirate = (self.truth_iterator_bitrate+1)%self.l
            
        self.truth_data[adaption_type][0][iterator] = par
        self.truth_data[adaption_type][1][iterator] = truth
        if iterator+1 == self.l:
            self.save('truth_'+adaption_type)
        
    def save(self, data):
        adaption_type = data.split('_')[1]
        data = data.split('_')[0]
        if(data == 'truth'):
            lines = zip(self.truth_data[adaption_type][0], self.truth_data[adaption_type][1])
        elif data == 'size':
            lines = zip(self.size_data[adaption_type][0], self.size_data[adaption_type][1])
        else:
            lines = zip(self.time_data[adaption_type][0], self.time_data[adaption_type][1])
        with open(data+adaption_type+'.csv', 'a') as writeFile:
            writer = csv.writer(writeFile)
            for line in lines:
                writer.writerow(line)
        writeFile.close()