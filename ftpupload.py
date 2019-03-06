import os.path, os
from ftplib import FTP, error_perm

host = 'student.coe.phuket.psu.ac.th'
port = 21

ftp = FTP()
ftp.connect(host,port)
ftp.login('s5835512005','43621266')
filenameCV = "save_images"
ftp.cwd("/public_html/test/pic")
def placeFiles(ftp, path):
    for name in os.listdir(path):
        localpath = os.path.join(path, name)
        if os.path.isfile(localpath):
            print("STOR", name, localpath)
            ftp.storbinary('STOR ' + name, open(localpath,'rb'))
        elif os.path.isdir(localpath):
            print("MKD", name)

            try:
                ftp.mkd(name)

                #ignore "directory already exists"
            except error_perm as e:
                if not e.args[0].startswith('550'): 
                    raise

            #print("CWD", name)
            #ftp.cwd(name)
            placeFiles(ftp, localpath)           
            #print("CWD", "..")
            #ftp.cwd("..")

placeFiles(ftp, filenameCV)

ftp.quit()