import cv2
import numpy as np
import math
import time
from queue import PriorityQueue

#Point class to create Point object
class Point:

    position=(0.,0.)
    g=0.0
    h=0.0
    f=0.0
    parent=None

    #constructor of the Point object
    def __init__(self,position):
        
        self.position=position

    #functions defining comparison operations between two Point object
    def __lt__(self,other):
        return self.f<other.f

    def __gt__(self,other):
        return self.f>other.f
        
        
#function to find source and destination point in the image        
def Find_Source_and_Dest(img,h,w):
  src_x,src_y,dest_x,dest_y=0,0,0,0

  for i in range(h):
    for j in range(w):
        if (img[i][j][0]==113 and img[i][j][1]==204 and img[i][j][2]==45):
            src_x=i
            src_y=j
        if (img[i][j][0]==60 and img[i][j][1]==76 and img[i][j][2]==231):
            dest_x=i
            dest_y=j

  return (src_x,src_y,dest_x,dest_y)

#function to check if index is within bounds
def isIndexValid(i,j,h,w):
    if ((i>=0 and i<h) and (j>=0 and j<w)):
        return True

    else:
        return False


#function to check if point is unblocked
def isUnblocked(i,j):
    if (img[i][j][0]!=255 or img[i][j][1]!=255 or img[i][j][2]!=255):

        return True

    else:
        return False


#function to calculate heuristic
def HValue(x,y):

    return max(abs(x-dest_x),abs(y-dest_y))


#function to return the final path
def return_path(img,current_cell):

    path=[]
    current=current_cell
    g=0.0
    
    while current is not None:
        path.append(current.position)
        par=current.parent

        if (current.position[0]!=src_x or current.position[1]!=src_y):
            g = g + math.sqrt(math.pow(current.position[0]-par.position[0],2)+math.pow(current.position[1]-par.position[1],2))
        
        current = par
        
    for val in path:
        img[val[0]][val[1]]=[10,10,240]
        
#print the total cost of the path       
    print("Cost of the path found: ",g)   
     
    return img  


#Function to find the shortest path using A Star algorithm
def AStar(img,h,w,src_x,src_y,dest_x,dest_y):

    
    #create the open point priority queue and the closed point list
    open_queue=PriorityQueue()
    cl_list=[]

    #create start point object
    st_pt = Point((src_x,src_y))
    st_pt.g,st_pt.h,st_pt.f = 0.0 ,0.0 ,0.0
    st_pt.parent=None

    #add starting point object to open queue
    open_queue.put((st_pt.f,st_pt))


    while (len(open_queue.queue)>0):

        #get the element with smallest 'f' from open queue and put it in closed list
        curr=(open_queue.get())[1]
        cl_list.append(curr)

        img[curr.position[0]][curr.position[1]]=(10,180,240)

        #if destination is found, return final image with path
        if (curr.position==(dest_x,dest_y)):
          
            img_final=return_path(img,curr)
            return img_final


        (i,j)=curr.position

        #create a child list
        ch_list=[]

        coeff=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

        #generate the current point's neighbours
        for (p,q) in coeff:

            if (isIndexValid(i+p,j+q,h,w)==True and isUnblocked(i+p,j+q)==True):

                ch_pt=Point((i+p,j+q))
                ch_pt.parent=curr
                ch_list.append(ch_pt)

        #check the children; if they are in closed list, skip them
        #if they are in open list and already have lesser 'f', skip them
        #if their values need updates, do it; else if it is new point, add it to open list
        for ch in ch_list:

            if len([x for x in cl_list if x.position==ch.position])>0 :
                continue
            
            ch.g = curr.g+ math.sqrt(math.pow(ch.position[0]-curr.position[0],2) +math.pow(ch.position[1]-curr.position[1],2))           
            ch.h=HValue(ch.position[0], ch.position[1])
            ch.f=ch.g+ch.h

            flag=0

            for item in open_queue.queue:

                if (item[1].position==ch.position):

                    flag=1
                    
                    if (item[1].g>=ch.g):

                        item[1].g=ch.g
                        item[1].f=ch.f
                        item[1].parent=curr

                    else:
                        continue    

            if (flag==0):

                open_queue.put((ch.f,ch))
                img[ch.position[0]][ch.position[1]]=(240,0,0)



#function to upscale the given image
def upscale(img,x,y,h,w):

    m,n=0,0
    upsc_img=np.zeros((x*h,y*w,3),dtype=np.uint8)

    for m in range(h):
        for n in range(w):

            for p in range(m*x,(m+1)*x):
                for q in range(n*y,(n+1)*y):

                    upsc_img[p][q]=img[m][n]

    return upsc_img
                    



#input the test image                    
img=cv2.imread(r"C:\Users\HP\OneDrive - iitkgp.ac.in\Desktop\AGV\Task 1\Images\Task_1_Low.png",1)

#reading the dimensions of the image
h,w,c=img.shape

#displaying an upscaled version of original image for reference
cv2.namedWindow("orig_image",cv2.WINDOW_AUTOSIZE)
img1=upscale(img, 10, 10, h, w)
cv2.imshow("orig_image",img1)
cv2.waitKey(0)

#create a new window to display the final image with the path shown
cv2.namedWindow("img_with_path",cv2.WINDOW_NORMAL)




#initialize variables to store the source and destination position
src_x,src_y,dest_x,dest_y=0,0,0,0   


#store the sorce and destination position
(src_x,src_y,dest_x,dest_y)=Find_Source_and_Dest(img, h, w)


#Note the start time
start=time.time()


#apply A* algorithm and reurn the modified image showing the required path
img=AStar(img,h,w,src_x,src_y,dest_x,dest_y)


#take the end time and print the time taken to find path
end=time.time()
print("The time taken to find the path : ",(end-start)," seconds")



#upscaling the image to (1000,1000) resolution
upscale_img=upscale(img,10,10,h,w)

#display the final image showing the path
cv2.imshow("img_with_path",upscale_img)
cv2.waitKey(0)
cv2.destroyAllWindows() 