#import libraries of python opencv
import cv2
import numpy as np
import os
import time
import datetime
import glob


file = open("./logfile/logfile.txt","w")
file2 = open("./logfile/position refer.txt","w")
file3 = open("./logfile/position change.txt","w")  
print ("Car Detection System Setting ...")
file.write("Car Detection System Active at " + datetime.datetime.now().strftime("%y/%m/%d - %H.%M.%S\n"))

#create VideoCapture object and read from video file
#cap = cv2.VideoCapture('./videos/cars.MP4')
cap = cv2.VideoCapture(0)

#use trained cars XML classifiers
car_cascade = cv2.CascadeClassifier('./cascade/cascade1.xml')

pic_num = 0

year = datetime.date.today().strftime("%Y")
mont = datetime.date.today().strftime("%m")

if not os.path.exists('save_images/'+year+'/'+mont):
           print ("Not Found Folder Save_images ...")
           os.makedirs('save_images/'+year+'/'+mont)
           print ("Created Folder Save_images  Success ...")
           file.write("Created Folder Save_images  Success  at  " + datetime.datetime.now().strftime("%y/%m/%d - %H.%M.%S\n"))

# Take the first frame and convert it to gray
ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)

print ("Status Ready ...")
file.write("Status Ready at " + datetime.datetime.now().strftime("%y/%m/%d - %H.%M.%S\n"))
print ("System Start ...")
file.write("Status System Start at " + datetime.datetime.now().strftime("%y/%m/%d - %H.%M.%S\n\n"))

def draw_flow(img, flow, step=20):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T  
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))

    for (x1, y1), (x2, y2) in lines:
    	file2.write("x1 = "+ str(x1)+"  "+"y1 = "+ str(y1)+"\t")
    	file3.write("x2 = "+ str(x2)+"  "+"y2 = "+ str(y2)+"\t")

    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis

#read until video is completed
while True:
    #capture frame by frame
    ret, frame = cap.read()

    #convert video into gray scale of each frames
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #detect cars in the video
    cars = car_cascade.detectMultiScale(gray, 2, 1)
    

    #to draw arectangle in each cars 
    for (x,y,w,h) in cars:
        car2 = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        

	  
    #save image     
    
    if cars is not None:
		print (" Detec found " + "  " +str(pic_num))
                cv2.putText(car2, "Object: "+str(pic_num), (x - 5, y - 5), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                crop_img = car2[y: y + h, x: x + w] 
                cv2.imwrite("save_images/"+year+"/"+mont+"/"+str(pic_num)+" - " +datetime.datetime.now().strftime("%y-%m-%d-%H-%M")+".jpg",crop_img) 
    #print str(pic_num) + "  "+"Save Success"+" "+datetime.datetime.now().strftime("%y/%m/%d - %H.%M.%S") +"\n"
    file.write(str(pic_num) + "  "+"Save Success"+" "+datetime.datetime.now().strftime("%y/%m/%d - %H.%M.%S") +"\n")
    file2.write(str(pic_num) + "  "+"Save Success"+" "+datetime.datetime.now().strftime("%y/%m/%d - %H.%M.%S") +"\n")
    file3.write(str(pic_num) + "  "+"Save Success"+" "+datetime.datetime.now().strftime("%y/%m/%d - %H.%M.%S") +"\n")
    pic_num += 1

    # Calculate the dense optical flow
    flow = cv2.calcOpticalFlowFarneback(prvs, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    rgbImg = draw_flow(gray, flow)


    #print cars
    #print flow.shape
    #print "Flow : : 0"
    #print flow[:][:][0]
    #print "Flow : : 1"
    #print flow[:][:][1]

    #display the resulting frame
    #cv2.imshow('video',  np.hstack((frame, rgbImg)))
    #cv2.imshow('Detect',frame)
    #cv2.imshow('flow',rgbImg)
    
    #press ESC or Q on keyboard to exit
    k = cv2.waitKey(30) & 0xff
    if k == 27 :
        break
    elif k == ord('q'):
        break


#release the videocapture object
cap.release()

#close all the frames
cv2.destroyAllWindows()
file.write("End System " +datetime.datetime.now().strftime("%y/%m/%d - %H.%M.%S\n\n"))
file.close()
file2.close()
file3.close()
print ("End System ... ")
