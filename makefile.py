import os
import datetime
import time

pic_num = 0

file = open("testfile.txt","a") 
file.write("Start System at " + datetime.datetime.now().strftime("%y/%m/%d - %H.%M.%S\n"))
file.write("Car Detection System Setting ...\n")
file.write("Start System at " + datetime.datetime.now().strftime("%y/%m/%d - %H.%M.%S\n"))
file.write("Status Ready at " + datetime.datetime.now().strftime("%y/%m/%d - %H.%M.%S\n"))
file.write("System Start at " + datetime.datetime.now().strftime("%y/%m/%d - %H.%M.%S\n\n"))
while True:
        pic_num += 1
	file.write("Detec found "+ "  " + str(pic_num) + "  " +datetime.datetime.now().strftime("%y/%m/%d - %H.%M.%S\n"))

file.write("Created Folder Save_images  Success  at  " + datetime.datetime.now().strftime("%y/%m/%d - %H.%M.%S\n\n"))

file.close() 
