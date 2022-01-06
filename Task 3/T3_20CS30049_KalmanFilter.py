import numpy as np
import matplotlib.pyplot as plt



#function to return the transpose of a matrix
def transpose(A,m,n,B):

    for i in range(n):
        for j in range(m):

            B[i][j]=A[j][i]


#reading the data file containing measured values as input          
inputFile = open(r"C:\Users\HP\OneDrive - iitkgp.ac.in\Desktop\AGV\Task 3\kalmann.txt")

#read the 1st line as input and obtain initial x and y coordinates
line=inputFile.readline()
posx_0,posy_0=line.split(',')

posx_0=float(posx_0)
posy_0=float(posy_0)

#initializing the state matrix with the initial positions
x_0=np.array([posx_0,posy_0,0.0,0.0])
x_0=np.reshape(x_0,(-1,1))
x=x_0

#initializing 2 lists to store the predicted points
x_coord=[posx_0]
y_coord=[posy_0]


#Time interval between measurements
t=1

#Initialize the dynamics matrix A
A=np.array([[1,0,t,0],[0,1,0,t],[0,0,1,0],[0,0,0,1]])


A_t = [[0 for i in range(4)] for j in range(4)]

#Taking transpose of A
transpose(A, 4, 4, A_t)


#Finding the matrix Q using the above parameters
Q=np.array([[5e-11,0,0,0],[0,1.2e-9,0,0],[0,0,1.3e-9,0],[0,0,0,1e-5]])

#Initializing the covariance matrix P representing the errors 
# in the parameters of the state vector
P=np.array([[10,0,0,0],[0,10,0,0],[0,0,10,0],[0,0,0,10]])

#Measuring matrix H which reads the values to be measured
H=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

H_t=[[0 for i in range (4)] for j in range(4)]

transpose(H,4,4,H_t)

#Transpose of H
H_t=np.array(H_t)

#Initializing the measurement noise covariance matrix R
R=np.array([[1.1e-6,0,0,0],[0,1e-6,0,0],[0,0,1.1e-6,0],[0,0,0,1e-6]])

#Identity matrix of 4*4
I=np.eye(4,dtype=float)

#Reading one line per iteration
for line in inputFile:
    
    #Storing position and velocity values in each line
    posx, posy, velx, vely = line.split(',')

    posx = float(posx)
    posy = float(posy)
    velx = float(velx)
    vely = float(vely)

    #Measurement matrix z
    z=np.array([posx, posy, velx, vely])
    z=np.reshape(z,(-1,1))

#x=A.x

    x=A.dot(x)

#P=APA'+Q
    P=np.add(A.dot(P.dot(A_t)), Q)
    P=np.reshape(P,(-1,4))


#Calculating difference between predicted and measured position values

    #y=z-H.x

    y=np.subtract(z,H.dot(x))
    y=np.reshape(y,(-1,1))


    #printing the updated positions and their uncertainty
    print(str(x[0][0])+" "+str(x[1][0])+"         "+str(y[0][0])+" "+str(y[1][0]))

    #storing the predicted points in 2 lists storing x and y coordinates
    x_coord.append(x[0][0])
    y_coord.append(x[1][0])

   #S=H.P.H' + R
    S=np.add(H.dot(P.dot(H_t)),R)
    S=np.reshape(S,(-1,4))

    #K=P.H'.S^(-1)
    K=P.dot(H_t.dot(np.linalg.inv(S)))
    K=np.reshape(K,(-1,4))

    #x=x+K.y

    x=np.add(x,K.dot(y)) 
    x=np.reshape(x,(-1,1))

#P=(I-K.H)*P
    P=(np.subtract(I,K.dot(H))).dot(P)
    P=np.reshape(P,(-1,4))

#closing the file
inputFile.close()

#plotting the points predicted by Kalman filer using matplotlib
plt.scatter(x_coord,y_coord,label="coordinates",color="blue",marker=".",s=30)

plt.xlabel('x-axis')
plt.ylabel('y-axis')

plt.title('Kalman filter points')

plt.legend()

plt.show()
