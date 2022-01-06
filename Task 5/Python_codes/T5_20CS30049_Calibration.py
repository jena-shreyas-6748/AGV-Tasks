import cv2
import os
import numpy as np
from numpy.linalg import norm

imgdir=r"C:\Users\HP\OneDrive - iitkgp.ac.in\Desktop\AGV\Task 5\Images"


imgPoints=np.zeros((7*7,1,2),np.float32)

objPoints=np.zeros((7*7,3),np.float32)
objPoints[ :,:2]=np.mgrid[0:7,0:7].T.reshape(-1,2)

count=0

mtx=np.zeros((3,3),np.float32)
dist=np.zeros((1,5),np.float32)


for filename in os.listdir(imgdir):

    f=os.path.join(imgdir,filename)
    img=cv2.imread(f,1)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    ret,corners=cv2.findChessboardCorners(gray,(7,7))

    if (ret==False):

        print("No corners detected for ",filename)
        continue


    corners_new=cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),(cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,30,0.001))
    imgPoints=corners_new

    objPoints=objPoints.reshape(1,-1,3)
    imgPoints=imgPoints.reshape(1,-1,2)

    objPoints=objPoints.astype('float32')
    imgPoints=imgPoints.astype('float32')

    if (count==0):
        
        ret,mtx,dist,rvecs,tvecs=cv2.calibrateCamera(objPoints,imgPoints,gray.shape[: :-1],None,None)
    else:
        ret,mtx,dist,rvecs,tvecs=cv2.calibrateCamera(objPoints,imgPoints,gray.shape[: :-1],mtx,dist)

    count=count+1
    print(count)


print("Camera matrix : ",mtx)
print("Distortion coefficients : ",dist)
