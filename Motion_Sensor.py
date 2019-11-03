#Importing the libraries
import cv2
from datetime import datetime as dt
import pandas as pd

first_frame=None                    #variable used in Line 25-26 to store the background image which is used to assess motion.
video=cv2.VideoCapture(0)           #Start webcam and recorder
motion_log=['dummy1','dummy2']      #List used to record the status of an object. 1 means the object was in the previous frame and 0 means the object was not in the previous frame. The dummy values are to avoid an error in line 43.
times_list=[]                       #Time of entry and exit is appended to this list

while True:
    check, frame=video.read()                               #read the current frame of the video
    status=0                                                #Will be changed to 1 when a big enough object enters the frame
    grey_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)       #convert the frame seen in 15 to 'GreyScale'
    grey_frame=cv2.GaussianBlur(grey_frame,(21,21),0)       #GaussianBlur helps supress the noise by using a Gaussian kernel. Refer "https://computergraphics.stackexchange.com/questions/39/how-is-gaussian-blur-implemented"
    
    #To assign the value of a background to the first_frame where necessary
    if first_frame is None:
        first_frame=grey_frame
        continue
    
    delta_frame=cv2.absdiff(first_frame,grey_frame)                             #calculate the difference between the current frame and the first frame (background)
    thresh_delta=cv2.threshold(delta_frame,50,255,cv2.THRESH_BINARY)[1]         #Whitens the area where the delta with backgrnd is greater than threshold. Returns a Tuple (recommends threshold value {N/A to THRESH_BINARY}, frame). Refer "https://docs.opencv.org/2.4/modules/imgproc/doc/miscellaneous_transformations.html?highlight=threshold"
    thresh_delta=cv2.erode(thresh_delta,None,iterations=2)                      #Useful for removing small white noises which helps detach two loosely connected objects.
    thresh_delta=cv2.dilate(thresh_delta,None,iterations=2,)                    #To increase object area and accentuate features. Erosion reduces area so it is followed by dilation. For more info refer "https://www.geeksforgeeks.org/erosion-dilation-images-using-opencv-python/"
    thresh_delta=cv2.morphologyEx(thresh_delta, cv2.MORPH_CLOSE,None)           #useful in closing small holes inside the foreground objects. Refer "https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html"
    
    #to differentiate between two or more separate objects which are adjacent in the dilated delta image
    (conts,_)=cv2.findContours(thresh_delta.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contour in conts:
        if cv2.contourArea(contour)<1500:        #To filter out any noise by removing the very small objects.
            continue
        else:
            status=1                            #When an object with contour area>1000 enters the frame. To be used to calculate motion time of the object
        
        #Draw a rectangle around the significant contours which show maximum difference when compared to the background/first_frame
        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    
    #Check the status of an object in the previous frame and append time to times_list if the previous status and current status change, indicating that an object has entered or exited the frame.
    motion_log.append(status)
    if motion_log[-1]!=motion_log[-2]:
        times_list.append(dt.now())

    #Create Windows to display all the frames
    cv2.imshow("Grey Frame",grey_frame)
    cv2.imshow("Delta Frame",delta_frame)
    cv2.imshow("Threshold Frame",thresh_delta)
    cv2.imshow("Grey Frame",frame)
    
    #Command to quit the application by pressing "q" or "Q"
    key=cv2.waitKey(1)
    if key==ord("q") or key==ord("Q"):
        if status==1:
            times_list.append(dt.now())
        break

#Stop recording and close the webcam windows
video.release()
cv2.destroyAllWindows()

#Create and export a DataFrame with the entry and exit times of an object
log_book=pd.DataFrame()
for i in range(0,len(times_list),2):
    log_book=log_book.append({"Object Entry Time":times_list[i],"Object Exit Time":times_list[i+1]},ignore_index=True)
log_book.to_csv('Motion_log_book.csv',index=False)


#################### CODE ENDS ####################