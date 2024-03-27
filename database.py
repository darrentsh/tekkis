import mysql.connector


class Database:
    def __init__(self) -> None:
        pass

    def insert_car_data(self, cursor, data):
        try:
            sql = (
                "INSERT INTO cars (model, price, year, mileage) VALUES (%s, %s, %s, %s)"
            )
            cursor.executemany(sql, data)
        except Exception as e:
            print(f"Error inserting car data: {e}")

    def create_database(self):
        mydb = mysql.connector.connect(
            host="localhost", user="LAPTOP-AO8BAO92", password="kyoebrn98"
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS cars_database")
