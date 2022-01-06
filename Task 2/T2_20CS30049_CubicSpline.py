import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

#initialize lists to store the data points
gr_pts=[]
x_coord=[]
y_coord=[]


while(True):

    pt=input("Enter a pt : ")

    #condition to break out of input loop
    if (pt=='x'):
        break

    pt=[float(a) for a in pt.split(",")]

    #adding the input data points to the lists
    gr_pts.append(pt)
    x_coord.append(pt[0])
    y_coord.append(pt[1])

#converting the lists into numpy array
gr_pts=np.array(gr_pts).T

x_coord=np.array(x_coord)
y_coord=np.array(y_coord)

#plotting only the data points
plt.plot(x_coord,y_coord,'ro')

plt.show()

#creating a 3rd order(cubic) spline fitting the given data points
tck,u = interpolate.splprep(gr_pts,k=3,s=0)

#it returns a smoothed out version of the polynomial curve 
out=interpolate.splev(np.linspace(0,1,100),tck,der=0)

#plot the final cubic spline
plt.plot(out[0],out[1],color='green')
plt.plot(gr_pts[0,:],gr_pts[1,:],'ro')
plt.show()


