import sys
import os
import matplotlib.pyplot as plt
import numpy as np
 
class nn_linear_layer:
    
    # linear layer.
    # randomly initialized by creating matrix W and bias b
    def __init__(self, input_size, output_size, std=1):         # I = 2, O = 4
        self.W = np.random.normal(0,std,(output_size,input_size)) # W (O x I)
        self.b = np.random.normal(0,std,(output_size,1)) # b (O x 1)
    
    ######
    ## Q1
    def forward(self,x): # x (B x I)
        y = (x @ self.W.T) + self.b.T # (B x I)*(I x O) => (B x O) + Broadcast (1 x O) => (B x O)
        return y
    
    ######
    ## Q2
    ## returns three parameters
    def backprop(self,x,dLdy): # dLdy (B x O)
        dLdW = dLdy.T @ x # (O x B) * (B x I) => (O x I)
        dLdx = dLdy @ self.W # (B x O) * (O x I) => (B x I)
        dLdb = dLdy.T @ np.ones((x.shape[0], 1)) # (O x B) * (B x 1) => (O x 1)
        return dLdW,dLdb,dLdx

    def update_weights(self,dLdW,dLdb):
        # parameter update
        self.W=self.W+dLdW
        self.b=self.b+dLdb

class nn_activation_layer: # I = O
    
    def __init__(self):
        pass
    
    ######
    ## Q3
    def forward(self,x): # x (B x I)
        sig = 1 / (1+np.exp(-1*x)) # (B x I)
        return sig
    
    ######
    ## Q4
    def backprop(self,x,dLdy): # dLdy (B x I)
        sig = 1 / (1+np.exp(-1*x))
        dLdx = dLdy * sig*(1-sig) # (B x I) (*) (B x I)
        return dLdx


class nn_softmax_layer:
    def __init__(self):
        pass
    ######
    ## Q5
    def forward(self,x): # x (B x I)
        softmax = np.exp(x) / np.sum(np.exp(x), axis = 1, keepdims=True) # (B x I)
        return softmax
    
    ######
    ## Q6
    def backprop(self,x,dLdy): # dLdy (B x O), O = I
        softmax = np.exp(x) / np.sum(np.exp(x), axis = 1, keepdims=True)
        dLdx = dLdy * softmax * (1-softmax) # (B x O) (*) (B x I) => (B x O)
        return dLdx

class nn_cross_entropy_layer:
    def __init__(self):
        pass
        
    ######
    ## Q7
    def forward(self,x,y): # x (B x 2) , y (B x 1)
        elem = -1*( (1-y) * np.log(x[:,0]) + y * np.log(x[:,1]) ) # (B x 1)
        Lce = np.sum(elem)/y.shape[0]
        return Lce
        
    ######
    ## Q8
    def backprop(self,x,y):
        m = x.shape[0]
        dLdx = np.zeros_like(x) # (B x 2) # if , x=(0.8,0.2) ? => y=0 나와야 정상 => y=0 이라면 grad=(0.8,0.2)-(1,0)=(-0.2,+0.2), y=1 이라면 grad=(0.8,0.2)-(0,1)=(0.8,-0.8)
        y = y.flatten()
        dLdx[:,0] = -1*(1-y)/x[:,0] + y/x[:,1]
        dLdx[:,1] = -1*y/x[:,1] + (1-y)/x[:,0]

        print(1/m * dLdx)

        return 1/m * dLdx # (B x 2)
    
    # y_real = 1 : (0.8,0.2) -> (0.0,1.0) "(0.8,-0.8)" // y_real = 0 : (0.8,0.2) -> (1.0,0.0) "(-0.2,0.2)" 

# number of data points for each of (0,0), (0,1), (1,0) and (1,1)
num_d=5

# number of test runs
num_test=40

## Q9. Hyperparameter setting
## learning rate (lr)and number of gradient descent steps (num_gd_step)
## This part is not graded (there is no definitive answer).
## You can set this hyperparameters through experiments.
lr=0.1  
num_gd_step=1000

# dataset size
batch_size=4*num_d

# number of classes is 2
num_class=2

# variable to measure accuracy
accuracy=0

# set this True if want to plot training data
show_train_data=True

# set this True if want to plot loss over gradient descent iteration
show_loss=True

################
# create training data
################

m_d1 = (0, 0)
m_d2 = (1, 1)
m_d3 = (0, 1)
m_d4 = (1, 0)

sig = 0.1
s_d1 = sig ** 2 * np.eye(2)

d1 = np.random.multivariate_normal(m_d1, s_d1, num_d)
d2 = np.random.multivariate_normal(m_d2, s_d1, num_d)
d3 = np.random.multivariate_normal(m_d3, s_d1, num_d)
d4 = np.random.multivariate_normal(m_d4, s_d1, num_d)

# training data, and has shape (4*num_d,2)
x_train_d = np.vstack((d1, d2, d3, d4))
# training data lables, and has shape (4*num_d,1)
y_train_d = np.vstack((np.zeros((2 * num_d, 1), dtype='uint8'), np.ones((2 * num_d, 1), dtype='uint8')))

if (show_train_data):
    plt.grid()
    plt.scatter(x_train_d[range(2 * num_d), 0], x_train_d[range(2 * num_d), 1], color='b', marker='o')
    plt.scatter(x_train_d[range(2 * num_d, 4 * num_d), 0], x_train_d[range(2 * num_d, 4 * num_d), 1], color='r',
                marker='x')
    plt.show()

################
# create layers
################

# hidden layer
# linear layer
layer1 = nn_linear_layer(input_size=2, output_size=4, )
# activation layer
act = nn_activation_layer()

# output layer
# linear
layer2 = nn_linear_layer(input_size=4, output_size=2, )
# softmax
smax = nn_softmax_layer()
# cross entropy
cent = nn_cross_entropy_layer()

# variable for plotting loss
loss_out = np.zeros((num_gd_step))

################
# do training
################

for i in range(num_gd_step):
    print('train step = ',i)
    # fetch data
    x_train = x_train_d
    y_train = y_train_d
        
    ################
    # forward pass
    
    # hidden layer
    # linear
    l1_out = layer1.forward(x_train)
    # activation
    a1_out = act.forward(l1_out)
    
    # output layer
    # linear
    l2_out = layer2.forward(a1_out)
    # softmax
    smax_out = smax.forward(l2_out)
    # cross entropy loss
    loss_out[i] = cent.forward(smax_out, y_train)
    
    ################
    # perform backprop
    # output layer
    # cross entropy
    b_cent_out = cent.backprop(smax_out, y_train)
    # softmax
    b_nce_smax_out = smax.backprop(l2_out, b_cent_out)
    
    # linear
    b_dLdW_2, b_dLdb_2, b_dLdx_2 = layer2.backprop(x=a1_out, dLdy=b_nce_smax_out)
    
    # backprop, hidden layer
    # activation
    b_act_out = act.backprop(x=l1_out, dLdy=b_dLdx_2)
    # linear
    b_dLdW_1, b_dLdb_1, b_dLdx_1 = layer1.backprop(x=x_train, dLdy=b_act_out)
    
    ################
    # update weights: perform gradient descent
    layer2.update_weights(dLdW=-b_dLdW_2 * lr, dLdb=-b_dLdb_2 * lr) #########################
    layer1.update_weights(dLdW=-b_dLdW_1 * lr, dLdb=-b_dLdb_1 * lr) #########################
    
    if (i + 1) % 2000 == 0:
        print('gradient descent iteration:', i + 1)

# set show_loss to True to plot the loss over gradient descent iterations
if (show_loss):
    plt.figure(1)
    plt.grid()
    plt.plot(range(num_gd_step), loss_out)
    plt.xlabel('number of gradient descent steps')
    plt.ylabel('cross entropy loss')
    plt.show()

################
# training done
# now testing

num_test = 100

for j in range(num_test):
    
    predicted = np.ones((4,))
    
    # dispersion of test data
    sig_t = 1e-2
    
    # generate test data
    # generate 4 samples, each sample nearby (1,1), (0,0), (1,0), (0,1) respectively
    t11 = np.random.multivariate_normal((1,1), sig_t**2*np.eye(2), 1)
    t00 = np.random.multivariate_normal((0,0), sig_t**2*np.eye(2), 1)
    t10 = np.random.multivariate_normal((1,0), sig_t**2*np.eye(2), 1)
    t01 = np.random.multivariate_normal((0,1), sig_t**2*np.eye(2), 1)
    
    # predicting label for test sample nearby (1,1)
    l1_out = layer1.forward(t11)
    a1_out = act.forward(l1_out)
    l2_out = layer2.forward(a1_out)
    smax_out = smax.forward(l2_out)
    predicted[0] = np.argmax(smax_out)
    print('softmax out for (1,1)', smax_out, 'predicted label:', int(predicted[0]))
    
    # predicting label for test sample nearby (0,0)
    l1_out = layer1.forward(t00)
    a1_out = act.forward(l1_out)
    l2_out = layer2.forward(a1_out)
    smax_out = smax.forward(l2_out)
    predicted[1] = np.argmax(smax_out)
    print('softmax out for (0,0)', smax_out, 'predicted label:', int(predicted[1]))
    
    # predicting label for test sample nearby (1,0)
    l1_out = layer1.forward(t10)
    a1_out = act.forward(l1_out)
    l2_out = layer2.forward(a1_out)
    smax_out = smax.forward(l2_out)
    predicted[2] = np.argmax(smax_out)
    print('softmax out for (1,0)', smax_out, 'predicted label:', int(predicted[2]))
    
    # predicting label for test sample nearby (0,1)
    l1_out = layer1.forward(t01)
    a1_out = act.forward(l1_out)
    l2_out = layer2.forward(a1_out)
    smax_out = smax.forward(l2_out)
    predicted[3] = np.argmax(smax_out)
    print('softmax out for (0,1)', smax_out, 'predicted label:', int(predicted[3]))
    
    print('total predicted labels:', predicted.astype('uint8'))
    
    accuracy += (predicted[0] == 0) & (predicted[1] == 0) & (predicted[2] == 1) & (predicted[3] == 1)
    
    if (j + 1) % 10 == 0:
        print('test iteration:', j + 1)

print('accuracy:', accuracy / num_test * 100, '%')






