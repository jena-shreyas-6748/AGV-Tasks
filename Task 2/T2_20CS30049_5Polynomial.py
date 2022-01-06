import numpy as np
import  matplotlib.pyplot as plt
from scipy import interpolate

#Polynomial class 
class Polynomial:

    x_0=np.zeros((2,3),dtype='float64')
    x_1=np.zeros((2,3),dtype='float64')
    coeff=np.zeros((6,1),dtype='float64')

    #constructor
    def __init__(self,x_0,x_1):

        self.x_0=x_0
        self.x_1=x_1

    #function to find quintic polynomial path joining the given initial and final states
    def FindPoly(self):

        
        p0,p1,p2,p3,p4,p5=0.,0.,0.,0.,0.,0.
        x0,y0,vx0,vy0,ax0,ay0,x1,y1,vx1,vy1,ax1,ay1=0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.

        y_x0,y_x1,y_xx0,y_xx1=0.,0.,0.,0.

        x0,y0   =x_0[0][0],x_0[1][0]
        vx0,vy0 =x_0[0][1],x_0[1][1]
        ax0,ay0 =x_0[0][2],x_0[1][2]

        x1,y1   =x_1[0][0],x_1[1][0]
        vx1,vy1 =x_1[0][1],x_1[1][1]
        ax1,ay1 =x_1[0][2],x_1[1][2]

        y_x0=vy0/vx0
        y_x1=vy1/vx1

        y_xx0=(vx0*ay0-ax0*vy0)/(vx0**3)
        y_xx1=(vx1*ay1-ax1*vy1)/(vx1**3)

        C= np.array([p0,p1,p2,p3,p4,p5]).reshape(6,1)

        Y= np.array([y0,y1,y_x0,y_x1,y_xx0,y_xx1]).reshape(6,1)

        A=np.array([[1,  x0,  x0**2,     x0**3,     x0**4,     x0**5],
                    [1,  x1,  x1**2,     x1**3,     x1**4,     x1**5],
                    [0,   1,   2*x0, 3*(x0**2), 4*(x0**3), 5*(x0**4)],
                    [0,   1,   2*x1, 3*(x1**2), 4*(x1**3), 5*(x1**4)],
                    [0,   0,      2,      6*x0,12*(x0**2),20*(x0**3)],
                    [0,   0,      2,      6*x1,12*(x1**2),20*(x1**3)]])

        A= np.reshape(A,(6,6))            

        C= (np.linalg.inv(A))@Y
        self.coeff=C
        return

    #function to find function value at given x
    def FnVal(self,x):

        a0=float(self.coeff[0][0])
        a1=float(self.coeff[1][0])
        a2=float(self.coeff[2][0])
        a3=float(self.coeff[3][0])
        a4=float(self.coeff[4][0])
        a5=float(self.coeff[5][0])

        return ((a0)+(a1)*x+(a2)*(x**2)+(a3)*(x**3)+(a4)*(x**4)+(a5)*(x**5))

    #function to find 1st derivative value at given x
    def Der1Val(self,x):

        a1=float(self.coeff[1][0])
        a2=float(self.coeff[2][0])
        a3=float(self.coeff[3][0])
        a4=float(self.coeff[4][0])
        a5=float(self.coeff[5][0])

        return ((a1)+2*(a2)*x+3*(a3)*(x**2)+4*(a4)*(x**3)+5*(a5)*(x**4))

    #function to find 2nd derivative value at given x
    def DerVal2(self,x):

        a2=float(self.coeff[2][0])
        a3=float(self.coeff[3][0])
        a4=float(self.coeff[4][0])
        a5=float(self.coeff[5][0])

        return (2*(a2)+6*(a3)*x+12*(a4)*(x**2)+20*(a5)*(x**3))

    #function to find 3rd derivative value at given x
    def DerVal3(self,x):

        a3=float(self.coeff[3][0])
        a4=float(self.coeff[4][0])
        a5=float(self.coeff[5][0])

        return (6*(a3)+24*(a4)*x+60*(a5)*(x**2))

    #function to find 4th derivative value at given x
    def DerVal4(self,x):
        
        a4=float(self.coeff[4][0])
        a5=float(self.coeff[5][0])

        return (24*(a4)+120*(a5)*x)

    #function to find 5th derivative value at given x
    def DerVal5(self,x):

        a5=float(self.coeff[5][0])

        return (120*(a5))



#enter the data values for initial and final states
ip=input("Enter the initial components of position, velocity and acceleration : ")
x_0=np.array([float(i) for i in ip.split(",")])
x_0=np.reshape(x_0,(3,2)).T

ip=input("Enter the final components of position, velocity and acceleration : ")
x_1=np.array([float(i) for i in ip.split(",")])
x_1=np.reshape(x_1,(3,2)).T

#create a polynomial object to store the quintic polynomial path joining initial and final states
poly=Polynomial(x_0,x_1)
poly.FindPoly()
print("Required polynomial is : ",poly.coeff[0][0]," +",poly.coeff[1][0],"*x +",poly.coeff[2][0],"*x^2 +",poly.coeff[3][0],"*x^3 +",poly.coeff[4][0],"*x^4 +",poly.coeff[5][0],"*x^5")

#Enter value of x to find function value and value of derivatives
x=input("Now enter value of x to find function value and value of derivatives at that point : ")
poly.FnVal(x)
poly.Der1Val(x)
poly.DerVal2(x)
poly.DerVal3(x)
poly.DerVal4(x)
poly.DerVal5(x)



