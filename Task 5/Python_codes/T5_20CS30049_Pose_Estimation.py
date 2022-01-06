import cv2
import os
import numpy as np
from numpy.linalg import norm
import imutils
from imutils.video import VideoStream
import time


#initializing a count variable    
count=0   

mtx=np.array([[825.25050601,0.,650.48955596],
[  0. ,806.66875505, 318.47075258 ],
[0. ,0. ,1.]])

print(type(mtx))

dist=np.array([[-1.50123365e-01, 3.76899822e+00, -2.85996284e-02, -5.28477925e-03, -1.74782836e+01]])
print(type(dist))

#calling the aruco dictionary from which the aruco tag in images can be obtained and hence finding 
#Aruco parameters
arucoDict=cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_100)
arucoParams=cv2.aruco.DetectorParameters_create()

#starting the video stream
vs=VideoStream(src=0).start()
time.sleep(2.0)

while True:

    #reading each frame of the video stream at regular intervals
    frame=vs.read()
    frame=imutils.resize(frame,width=1000)

    (corners,ids,rejected)=cv2.aruco.detectMarkers(frame,arucoDict,parameters=arucoParams)

    imgPoints=[]

    if (len(corners)>0):
        ids.flatten()
    for (markerCorner,markerID) in zip(corners,ids) :

        #finding the corners of the Aruco tag
        corners=markerCorner.reshape((4,2))
        (topLeft,topRight,bottomRight,bottomLeft)=corners

        
        topRight=np.array([int(topRight[0]),int(topRight[1])])
        topLeft=np.array([int(topLeft[0]),int(topLeft[1])])
        bottomRight=np.array([int(bottomRight[0]),int(bottomRight[1])])
        bottomLeft=np.array([int(bottomLeft[0]),int(bottomLeft[1])])

        #adding corners to imagePoints
        imgPoints.append(topLeft)
        imgPoints.append(topRight)
        imgPoints.append(bottomRight)
        imgPoints.append(bottomLeft)

        #highlighting the centre point of the Aruco tag
        cX=int((topLeft[0]+bottomRight[0])/2.0)
        cY=int((topLeft[1]+bottomRight[1])/2.0)
        cv2.circle(frame,(cX,cY),4,(0,0,255),-1) 

        #highlighting the borders of the Aruco tag
        cv2.line(frame,topLeft,topRight,(0,255,0),2)
        cv2.line(frame,bottomRight,topRight,(0,255,0),2)
        cv2.line(frame,topLeft,bottomLeft,(0,255,0),2)
        cv2.line(frame,bottomLeft,bottomRight,(0,255,0),2)
        

        cv2.putText(frame,str(markerID),(topLeft[0],topLeft[1]-15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)


    imgPoints=np.array(imgPoints)

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #finding the object points
    objPoints=np.array( [np.array([0.,0.,0.]),np.array([1.0,0.,0.]),np.array([1.0,-1.0,0.]),np.array([0.,-1.0,0.])] )

    objPoints=objPoints.reshape(1,-1,3)
    imgPoints=imgPoints.reshape(1,-1,2)

    objPoints=objPoints.astype('float32')
    imgPoints=imgPoints.astype('float32')

    #estimating pose using the following function 

    rvecs,tvecs,_ = cv2.aruco.estimatePoseSingleMarkers(imgPoints,0.102,mtx,dist)

    #finding the translation vector wrt Aruco tag frame
    tvecs=np.array(tvecs)
    tvecs=np.multiply(tvecs,-1)

    #finding the rotation vector wrt Aruco tag frame
    rvecs=np.array(rvecs)
    (rmtx,jacobian)=cv2.Rodrigues(rvecs)
    rmtx=np.linalg.inv(rmtx)
    (rvecs,jacobian)=cv2.Rodrigues(rmtx)

    #printing the required parameters for pose estimation
        

    print("Height of camera : ",abs(tvecs[0][0][1]*100.0)," cm")
    print("Distance of camera from Aruco tag : ",norm(tvecs)*100.0," cm")

    print("Roll : ",rvecs[0][0]*180/3.14159," degrees")
    print("Pitch : ",rvecs[1][0]*180/3.14159," degrees")
    print("Yaw : ",rvecs[2][0]*180/3.14159," degrees")



        

    #showing the frame with highlighted Aruco tags    
    cv2.imshow("frame",frame) 
    key=cv2.waitKey(50) & 0xFF

            
cv2.destroyAllWindows()
vs.stop()

