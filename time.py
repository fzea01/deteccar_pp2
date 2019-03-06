import time
import datetime
import cv2

#while True:

print "Time in seconds since the epoch: %s" %time.time()
print "Current date and time: " , datetime.datetime.now()
print "Or like this: " ,datetime.datetime.now().strftime("%y/%m/%d - %H.%M.%S")


print "Current year: ", datetime.date.today().strftime("%Y")
print "Current Month: ", datetime.date.today().strftime("%m")

print "Month of year: ", datetime.date.today().strftime("%B")
print "Week number of the year: ", datetime.date.today().strftime("%W")
print "Weekday of the week: ", datetime.date.today().strftime("%w")
print "Day of year: ", datetime.date.today().strftime("%j")
print "Day of the month : ", datetime.date.today().strftime("%d")
print "Day of week: ", datetime.date.today().strftime("%A")

	#k = cv2.waitKey(30) & 0xff
   	#if k == 27 :
      	#    break
   	#elif k == ord('q'):
        #    break	
