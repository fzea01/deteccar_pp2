#import libraries of python opencv
import cv2
import numpy as np
import os
import time
import datetime
import glob
import mysql.connector
import Adafruit_DHT
#import multitasking
import signal

# kill all tasks on ctrl-c
#signal.signal(signal.SIGINT, multitasking.killall)


print ("Car Detection System Setting ...")
sensor = Adafruit_DHT.AM2302
pin = 2
pic_num = 1
count = 0
car2 = None
year = datetime.date.today().strftime("%Y")
mont = datetime.date.today().strftime("%m")

if not os.path.exists('save_images/'+year+'/'+mont):
           print ("Not Found Folder Save_images ...")
           os.makedirs('save_images/'+year+'/'+mont)
           print ("Created Folder Save_images  Success ...")

try:
    connection = mysql.connector.connect(host='student.coe.phuket.psu.ac.th',
                             database='s5835512005_403',
                             user='s5835512005_403',
                             password='aw38KA43')
    cur = connection.cursor()
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Succesfully Connected to MySQL database. MySQL Server version on ", db_Info)
except Error as e:
    print("Error while connecting to MySQL", e)

           
#@multitasking.task # <== this is all it takes :-)
def temp():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        #print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        print('Put Temp={0:0.1f}*C To DB'.format(temperature))
    else:
        print('Failed to get reading. Try again!')
    degrees = str(temperature)
    sql = """INSERT INTO `Temp` (`Idtmp`, `Value`, `Dt`) VALUES (NULL, "{}", CURRENT_TIMESTAMP);""".format(degrees[0:4])
    cur.execute(sql)
    connection.commit()
    os.system('python ftpupload.py')
	
#@multitasking.task # <== this is all it takes :-)
def draw_flow(img, flow, step=60):
    try:
        h, w = img.shape[:2]
        y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
        fx, fy = flow[y,x].T  
        lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
        lines = np.int32(lines + 0.5)
        vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cv2.polylines(vis, lines, 0, (0, 255, 0))
    
        for (x1, y1), (x2, y2) in lines:
            cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
            cv2.arrowedLine(frame, (x1,y1), (x2,y2), (0,0,255), 1) ##red
            if (y2-y1)>1:
                #print "FLOW POS"
                print y2-y1
                cars = car_cascade.detectMultiScale(gray, 2, 1)
                for (x,y,w,h) in cars:
                    print "Dpetec found " + "  " + str(pic_num)
                    cv2.imwrite("save_images/"+year+"/"+mont+"/"+str(pic_num)+" - " +datetime.datetime.now().strftime("%y-%m-%d-%H-%M")+".jpg",frame)
                    pic_num += 1
    except ValueError:
        print('You cancelled the operation.')

      
    return vis


#create VideoCapture object and read from video file
cap = cv2.VideoCapture()
cap.open('rtsp://admin:admin@172.19.59.10:554/live_st1')
#use trained cars XML classifiers
car_cascade = cv2.CascadeClassifier('./cascade/cascade1.xml')

# Take the first frame and convert it to gray
ret, frame1 = cap.read()
frame1 = cv2.resize(frame1, (600, 400))
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)

print ("Status Ready ...")
print ("System Start ...")


#read until video is completed
while True:
    
    try:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (600, 400))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        #cars = car_cascade.detectMultiScale(gray, 2, 1)
        
    #to draw arectangle in each cars 
        #for (x,y,w,h) in cars:
            #car2 = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    #save image     
        #for (x,y,w,h) in cars:
            #if cars is not None:
                        #print "Detec found " + "  " + str(pic_num)
                        #crop_img = car2[y: y + h, x: x + w] 
                        #cv2.imwrite("save_images/"+year+"/"+mont+"/"+str(pic_num)+" - " +datetime.datetime.now().strftime("%y-%m-%d-%H-%M")+".jpg",frame)
                        
                        
			#print str(pic_num) + "  "+"Save Success"+" "+datetime.datetime.now().strftime("%y/%m/%d - %H.%M.%S") +"\n"
            #pic_num += 1

    # Calculate the dense optical flow
        flow = cv2.calcOpticalFlowFarneback(prvs, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        rgbImg = draw_flow(gray, flow)
        
        if count>30:
            temp()
            count = 0
            pic_num = 1
            
        count += 1
    
	#display the resulting frame
        cv2.imshow('Detect',frame)
        
		
    #press ESC or Q on keyboard to exit
        k = cv2.waitKey(30) & 0xff
        if k == 27 :
            break
        elif k == ord('q'):
            break
        
    except ValueError:
        print('You cancelled the operation.')
        cap.release()
	connection.close() 

temp()
cv2.destroyAllWindows()
cap.release()
connection.close()
print ("End System ... ")