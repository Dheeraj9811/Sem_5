import matplotlib.pyplot as plt
import numpy as np
class NN():
  """
  Neural Network Classifier 
  """
  def __init__(self, num_layers, layer_size, activation, lr, weightinit, batch_size, epochs):
    self.num_layers, self.layer_size, self.activation, self.lr, self.weightinit, self.batch_size, self.epochs = num_layers, layer_size, activation, lr, weightinit, batch_size, epochs

  def activationfn(self,X):
    string=f"self.{self.activation}(X)"    
    return eval(string)

  def gradfn(self,X):
    string=f"self.{self.activation}_grad(X)"    
    return eval(string)

  def score(self, X, y):
    y_pred = self.predict(X)
    counter=0
    for i in range(len(y_pred)):
      if(y_pred[i]==y):
        counter+=1
    return counter/len(y)

  def initialization(self):
    """
    We make matrices of (layer_size[i], layer_size[i+1]) as we need
    Wji as the params, all combinations that are possible.
    """
      
      
    params = {}
    mylayers = self.layer_size
    
    for i in range(0,self.num_layers-1):
        params["b" + str(i+1)] = np.zeros((1,mylayers[i+1]))


        if(self.weightinit == 'normal'):
          thislayer = np.random.normal(size = (mylayers[i],mylayers[i+1]))*0.01
          
        elif(self.weightinit == 'zero'):
          thislayer = np.zeros((mylayers[i],mylayers[i+1]))

        else:
          thislayer = np.random.rand(mylayers[i],mylayers[i+1])*0.01

        params["W" + str(i+1)] = thislayer
        

    self.params = params

  def crossentropyloss(self, Amatrix, Y):
      temp=Amatrix[np.arange(len(Y)), Y.argmax(axis=1)]
      temp=np.where(temp>0.000000000000001,temp,0.000000000000001)
      logp = - np.log(temp)
      celoss = np.sum(logp)/len(Y)
      return celoss

  def forward_prop(self,X,params):
      
      A = X
      myactivations = {}
      before_activation = {}
      numhiddenlayers=self.num_layers-2
      for i in range(numhiddenlayers):
          A_prev = A
          Z = np.dot(A_prev, params["W" + str(i+1)]) + params["b" + str(i+1)]
          before_activation["Z" + str(i+1)] = Z
          A=self.activationfn(Z)
          myactivations["A" + str(i+1)] = A           
          A_prev = A
      
      
      ZL = np.dot(A_prev, params["W" + str(numhiddenlayers+1)]) + params["b" + str(numhiddenlayers+1)]        
      AL = (np.exp(ZL)/(np.sum(np.exp(ZL),axis = 1, keepdims = True)))  # SoftMax
      myactivations["A" + str(numhiddenlayers+1)] = AL
      before_activation["Z" + str(numhiddenlayers+1)] = ZL

      return AL, myactivations, before_activation
  def backward_prop(self, X, Y, before_activation, myactivations):
      """
      Complete Backward Prop
      """
      gradients = {}
      Lay = self.num_layers-1
      myactivations["A0"] = X

      
      A = myactivations["A" + str(Lay)]
      dZ = A - Y

      dW = np.dot(myactivations["A" + str(Lay-1) ].T, dZ)/len(X)
      db = np.sum(dZ, axis=0, keepdims=True) / len(X)
      dAp = np.dot(dZ, self.params["W" + str(Lay)].T)
    
      gradients["db" + str(Lay)] = db
      gradients["dW" + str(Lay)] = dW

      for l in range(Lay - 1, 0, -1):
          dGrad=self.gradfn(before_activation["Z" + str(l)])          
          dZ = dAp * dGrad
          dW = (1/len(X)) * np.dot(myactivations["A" + str(l - 1)].T, dZ)
          db = (1/len(X)) * np.sum(dZ, axis=0, keepdims=True)
          if l > 1:
            dAp = np.dot(dZ,self.params["W" + str(l)].T)
          gradients["dW" + str(l)] = dW
          gradients["db" + str(l)] = db
          
      #Update the params
      for i in range(Lay):
          self.params["W" + str(i+1)] -= self.lr*gradients["dW" + str(i+1)]
          self.params["b" + str(i+1)] -= self.lr*gradients["db" + str(i+1)]



      
  
  def fit(self, X, y, x_val, y_val):
      """
      Train the model.
      """
      self.initialization()
      self.classes=int(np.max(y))
      m=X.shape[0]
      y = self.converttoprobvsclassmatrix(y)

      train_losses = []
      val_losses = []
      
      
      noofbatches=m//self.batch_size
      combined_train_data=[]

      for i in range(0,noofbatches):
        myX=X[self.batch_size*i:self.batch_size*(i+1),:]
        myY=y[self.batch_size*i:self.batch_size*(i+1),:]
        combined_train_data.append((myX,myY))

      

      for epoch in range(self.epochs):
          print(f"Epoch: {epoch+1} ", end='' )
          trainbatchloss = []
          valbatchloss = []
      
          for batch_x, batch_y in combined_train_data:
              A, activations, preactivations = self.forward_prop(batch_x,self.params)
              train_cost = self.crossentropyloss(A,batch_y)
              trainbatchloss.append(train_cost)
              self.backward_prop(batch_x,batch_y,preactivations, activations )
              proba = self.predict_proba(x_val)
              valloss = self.crossentropyloss(proba, self.converttoprobvsclassmatrix(y_val))
              valbatchloss.append(valloss)
          


          train_losses.append(np.array(trainbatchloss).mean())
          val_losses.append(np.array(valbatchloss).mean())
              
              
      
      self.train_losses = train_losses
      self.val_losses = val_losses
      

  def converttoprobvsclassmatrix(self, y):
      m = len(y)
      myy = np.zeros((int(m),self.classes+1))
      for i in range(m):
          l = int(y[i])
          myy[i,l] = 1
      return myy
  def predict_proba(self, inp_X):
    proba,temp,temp2 = self.forward_prop(inp_X,self.params)
    return proba
  def predict(self, X):
    proba = self.predict_proba(X)
    y_pred = np.argmax(proba, axis = 1)
    return y_pred

  def score(self, X, y):
    y_pred = self.predict(X)
    counter=0
    
    for i in range(len(y_pred)):
      if(y_pred[i]==y[i]):
        counter+=1
    return counter/len(y)

  def relu(self, X):
    return X * (X>=0)
  
  def relu_grad(self, X):
    return 1*(X>=0)
  
  def leakyrelu(self, X):
    return np.where(X > 0, X, X * 0.01)
  def leakyrelu_grad(self,z):
    f = np.maximum(z, 0.01*z)
    grad = np.where(f>0, 1, 0.01)
    return grad


  def sigmoid(self, X):
    return 1/(1+np.exp(-X))

  def sigmoid_grad(self, X):
    return self.sigmoid(X) *(1-self.sigmoid (X))

  def linear(self, X):
    return X

  def linear_grad(self, X):
    return np.ones(X.shape)

  def tanh(self, X):
    return np.tanh(X)

  def tanh_grad(self, X):
    return 1-self.tanh(X)*self.tanh(X)

  def softmax(self, X):
    exp = np.exp(X)
    return exp/(np.sum(exp,axis = 1, keepdims = True))

  def softmax_grad(self, X):
    return self.softmax(X) *(1-self.softmax(X))