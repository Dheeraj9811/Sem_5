import matplotlib.pyplot as plt
import pandas as pd
import random 
import numpy as np
from matplotlib import figure

class Perceptron:

    def __init__(self,X_actual,Y_actutal, learning_rate=0.01, epochs=1000):
        # declearing varibles
        self.lr = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None
        self.X_actual = X_actual
        self.Y_actutal = Y_actutal
    
  


    def learning(self, X, Y,flag=0):
        row, n_features = X.shape
        # x is here your feature matirx n*m

        # init weight parameters with zeros and bias = 0
        self.weights = np.zeros(n_features)
        self.bias = 0

        # y_ = np.array([1 if i > 0 else 0 for i in y])
        Y = np.array(Y)
        # print(Y)
        for _ in range(self.epochs):
            # taking loop i for index and value at that index
            for j in range(len(X)):
                # print(type(val), val)
                
                # print("----")

                # print(self.bias)
                temp_y_predic = np.dot(X[j], self.weights) + self.bias
                y_pred = self.step_func(temp_y_predic)
                
                #  update rule 
                update = self.lr * (Y[j] - y_pred)
                
                # updating weights
                self.weights += update * X[j]
                #according to question if falg = 1 then bais = 0 everytime
                if(flag == 1):
                    self.bias =0
                else:
                    self.bias += update
                
        return self.weights, self.bias
    
    
    # tesing function for own satisfication
    def predict(self, X):
        temp_y_predic = np.dot(X, self.weights) + self.bias
        y_pred = self.step_func(temp_y_predic)
        return y_pred
    # activator function here we are using step function
    def step_func(self, x):
        if x>=0:
            return 1
        else:
            return 0


    
class dataset:
    N_points =0
    df = pd.DataFrame()
    data0 =[]
    data1 =[]

    def helperl0_y(self,x,r):
        y1 = (r**2 -x**2)**0.5
        y2 = -(r**2 -x**2)**0.5
        return y1, y2
    
    def helperl1_y(self, x, h, k, r):
        y1 = (r**2 - (x-h)**2 )**0.5 + k
        y2 = -((r**2 - (x-h)**2 )**0.5) + k
        # print(y2)
        return y1,y2
    
    def __init__(self, N_points):
        self.N_points =N_points
        self.data0=(self.calculate_l0(self.N_points)).copy()
        
        self.data1 = self.calculate_l1(self.N_points).copy()
        # print(self.data0)

    def calculate_l0(self, N_points):
        h = 0
        k = 0
        r = 1
        print(r)
        
        data = []
        for i in range(N_points//4):
            x = random.uniform(-1,1)
            y1, y2 = self.helperl0_y(x,r)
            temp = [x, y1,0]  # adding x ,y , label
            data.append(temp)

            temp = [x, y2,0]  # adding x ,y , label
            data.append(temp)

        # print(data)
        return data

    def calculate_l1(self, N_points):
        h = 0
        k = 3
        r = 1
        i = 0
        data = []
        for i in range(N_points//4):
            x = random.uniform(-1,1)
            y1 ,y2 = self.helperl1_y(x, h, k, r)
            temp = [x,y1,1]  # adding x ,y , label = 1
            temp1 =[x,y2,1]
            data.append(temp)
            data.append(temp1)
            # print(data)
            # print("")

        
        return data
    # get function will return  df according to question  which we will call in main
    def get(self,add_nose = False):
        if(add_nose == False):
            # print("data0",self.data1)
            # print("new rand",self.data0)
            random.shuffle(self.data0)
            random.shuffle(self.data1)
            self.df = pd.DataFrame(self.data0,columns=['X','Y','Label'])
            df1 = pd.DataFrame(self.data1,columns=['X','Y','Label'])
            self.df=self.df.append(df1,ignore_index = True)
            # print("data0",self.data0)
            # print(df1.head())
        else:
            random.shuffle(self.data0)
            random.shuffle(self.data1)
            self.df = pd.DataFrame(self.data0,columns=['X','Y','Label'])
            df1 = pd.DataFrame(self.data1,columns=['X','Y','Label'])
            self.df=self.df.append(df1,ignore_index = True)
            lable = self.df.iloc[:,-1]
            
            # print(lable)
            mean = 0
            sigma = 0.1
            noise = pd.DataFrame(np.random.normal(mean,sigma,[len(self.df),2]),columns=['X','Y'])
            # print(noise.head())
            # print("-------------------")
            # print(self.df.head())
            # print("-------------------")


            self.df=self.df.loc[:,self.df.columns != 'Label'].add(noise)
            self.df["Label"] = lable 
            # print(self.df.head())
        return self.df