from seleniumbase import Driver
from scrape import Scrape
from database import Database  # , DatabaseConnection
from api import API
import mysql.connector


def scrape_cars(first_page, last_page):
    browser = Driver(uc=True)
    db = Database()
    db.create_database()

    scrape = Scrape()

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="LAPTOP-AO8BAO92",
            password="kyoebrn98",
            database="cars_database",
        )

        with conn.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS cars (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    model TEXT, 
                    price TEXT, 
                    year INT, 
                    mileage TEXT
                )"""
            )

            for i in range(first_page, last_page):
                car_data = scrape.scrape_car_data(browser, i)
                try:
                    db.insert_car_data(cursor, car_data)
                except mysql.connector.ProgrammingError as err:
                    print(err)
                print(f"Scraped page {i}")
            conn.commit()

    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")
    finally:
        conn.close()
        browser.close()
