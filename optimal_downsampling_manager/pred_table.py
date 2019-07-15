from sklearn import neural_network
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import r2_score, mean_squared_error
import pickle
import numpy as np
import sys
import pandas as pd
import datetime
import csv

class Pred_Table():
    def __init__(self):
        self.pred_table={}
        self.time_model = None
        self.targetNum_model = None
        self.target_std = None
        self.df = None
    
    def parse_name(self,video_name):
        info = video_name.split('_')
        machine = info[1]
        date=info[2].split('-')
        weekday = str(datetime.datetime(int(date[0]),int(date[1]),int(date[2])).strftime("%w"))
        m = info[3].split(':')
        min_ = int(m[0])*60+int(m[1])

        return machine,weekday,min_
    
    
    def get_pred_targetNum_GT(self, video_name,frames_num,sample_rate):
        
        machine,weekday,min_ = self.parse_name(video_name)
        x_df1 = pd.get_dummies(pd.DataFrame({
              'machine':[str(machine)],
              'weekday':[str(weekday)],
              'minute':[min_],
              'frames':[frames_num],
              'sample_rate':[sample_rate]
             }))
        
        if self.df is not None:
            x = x_df1.reindex(columns = self.df.columns,fill_value=0).values.astype(float)
        else:
            raise Exception('dataFrame has not been set')
        
        if self.target_std is not None:
            x[:,:3] = self.target_std.transform(x[:,:3])
        else:
            raise Exception('stdizer has not been set')
        
        y = self.targetNum_model.predict(x)
        if y[0]<=0:
            return 0.001
        else:
            return y[0]

    def target_regression(self, dataSet_path='dataSet/dataSet_8.csv', check_score=True):
        # reshape the target
    
        raw_data = pd.read_csv(dataSet_path)
        
        names = raw_data.drop(['frames','sample_rate','targetNum','time'], axis = 1).values
        names=np.reshape(names,(names.shape[0],))
        
        # split the data which is needed for regression
        with open('dataSet/processed_data.csv','w',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['machine','weekday','minute','frames','sample_rate','targetNum'])
            for i,video_name in enumerate(names):
                machine,weekday,min_ = self.parse_name(video_name)
                row = [
                        machine,weekday,
                        min_,
                        raw_data['frames'][i],
                        raw_data['sample_rate'][i],
                        raw_data['targetNum'][i]
                      ]
                writer.writerow(row)
        
        # fit the model
        df = pd.read_csv('dataSet/processed_data.csv')
        X = df.drop(['targetNum'], axis = 1)
        y = df['targetNum'].values
        cat_feature=['machine','weekday']

        X = pd.get_dummies(X,columns=cat_feature)
        
        self.df = X.iloc[[0]] # save dataFrame for new input one-hot coding
        
        X = X.values.astype(float)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2,random_state = 0)
        
        # Standardize is important to fit this model
        self.target_std = StandardScaler() # save the std scaler (before inferencing the data, we need to std it first)
        self.target_std.fit(X_train[:,:3])

        X_train[:,:3]=self.target_std.transform(X_train[:,:3])
        X_test[:,:3]=self.target_std.transform(X_test[:,:3])

        # start to train regression model
        mlp = neural_network.MLPRegressor(hidden_layer_sizes=(20,10), activation="relu",
                 solver='adam', alpha=0.0001,
                 batch_size=10, learning_rate="constant",
                 learning_rate_init=0.01,
                 power_t=0.5, max_iter=200,tol=1e-4)

        mlp.fit(X_train,y_train)
        
        self.targetNum_model = mlp # save the model
        
        
        if check_score:
            y_train_pred = mlp.predict(X_train)
            y_test_pred = mlp.predict(X_test)

            print('------predicting target model performance-----')
            print('(MSE) train: %.2f, test: %.2f'%(mean_squared_error(y_train,y_train_pred), 
                                                   mean_squared_error(y_test,y_test_pred)))
            print('(R^2) train: %.2f, test: %.2f'%(r2_score(y_train,y_train_pred), 
                                                   r2_score(y_test,y_test_pred)))

        
    def get_pred_time(self,sample_rate):
        try:
            if self.time_model is not None:
                y_test_pred = self.time_model.predict(np.asarray(sample_rate).reshape([-1,1]))
        except ModelError:
            print("Not yet set model !")
            
        return y_test_pred[0]

    def	time_regression(self,dataSet_path='dataSet/dataSet_8.csv',check_score=True):
                
                        
        df = pd.read_csv(dataSet_path)
        df = shuffle(df)
        X = df.drop(['video_name','time','frames'], axis = 1).values

        y = df['time'].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2,random_state = 0)
        
        # start to train regression model
        mlp = neural_network.MLPRegressor(hidden_layer_sizes=(10), activation="relu",
                 solver='adam', alpha=0.0001,
                 batch_size=10, learning_rate="constant",
                 learning_rate_init=0.01,
                 power_t=0.5, max_iter=200,tol=1e-4)
        mlp.fit(X_train,y_train)
        
        self.time_model = mlp
        if check_score:
            y_train_pred = mlp.predict(X_train)
            y_test_pred = mlp.predict(X_test)

            print('-----predicting time model performance-----')
            print('(MSE) train: %.2f, test: %.2f'%(mean_squared_error(y_train,y_train_pred), 
                                                   mean_squared_error(y_test,y_test_pred)))
            print('(R^2) train: %.2f, test: %.2f'%(r2_score(y_train,y_train_pred), 
                                                   r2_score(y_test,y_test_pred)))
    def save_table(self):
        with open("dataSet/pred_table.pickle", "wb") as file_:
            pickle.dump(self, file_, -1)
        

pred = Pred_Table()
pred.time_regression()
pred.target_regression()
pred.save_table()