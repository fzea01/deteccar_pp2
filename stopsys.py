import mysql.connector

try:
    connection = mysql.connector.connect(host='student.coe.phuket.psu.ac.th',
                             database='s5835512005_403',
                             user='s5835512005_403',
                             password='aw38KA43')
    cur = connection.cursor()
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Succesfully Disconnected System")
except Error as e:
    print("Error while connecting to MySQL", e)

sql = """UPDATE `Status` SET `State` = 'STOP' WHERE `Status`.`IdSt` = 1;"""
cur.execute(sql)
connection.commit()

sql = """UPDATE `Status` SET `State` = 'OFF' WHERE `Status`.`IdSt` = 2;"""
cur.execute(sql)
connection.commit()

sql = """UPDATE `Status` SET `State` = 'STOP' WHERE `Status`.`IdSt` = 3;"""
cur.execute(sql)
connection.commit()

connection.close()           



