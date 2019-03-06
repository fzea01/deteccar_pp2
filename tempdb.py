import mysql.connector
import Adafruit_DHT
import time

sensor = Adafruit_DHT.AM2302

pin = 2

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


humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
degrees = str(temperature)
sql = """INSERT INTO `Temp` (`Idtmp`, `Value`, `Dt`) VALUES (NULL, "{}", CURRENT_TIMESTAMP);""".format(degrees[0:4])
cur.execute(sql)
connection.commit()
connection.close()           

