
import mysql.connector
mydb = mysql.connector.connect(
            host='localhost', user="LAPTOP-AO8BAO92", password="kyoebrn98"
        )
mycursor = mydb.cursor()
print(mycursor)
