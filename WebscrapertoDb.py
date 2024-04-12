import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import re
import time

def find_word_before_decimal(text):
    pattern = re.compile(r"\d+\.\d+")
    match = pattern.search(text)
    if match:
        index_a = match.start()
        word_before_a = text[: index_a + 3]
        return word_before_a
    else:
        return text


def scrape_car_data(browser, page_num):
    try:
        browser.get(f"https://www.mudah.my/malaysia/cars-for-sale?o={page_num}")
        car_list = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, '[data-testid^="listing-ad-item-"]')
            )
        )
        time.sleep(5)
        for car in car_list:
            car_brand_model = find_word_before_decimal(
                car.find_element(By.TAG_NAME, "a").get_attribute("title")
            )
            car_price = re.findall(re.compile("RM \d+,\d+"), car.text)[0]
            try:
                car_year = car.find_element(
                    By.CSS_SELECTOR, '[title="Manufactured Year"]'
                ).get_attribute("innerText")
            except NoSuchElementException:
                car_year = car.find_element(
                    By.CSS_SELECTOR, '[data-testid="year-verified-badge"]'
                ).get_attribute("innerText")
            car_mileage = car.find_element(
                By.CSS_SELECTOR, '[title="Mileage"]'
            ).get_attribute("innerText")
            yield (car_brand_model, car_price, car_year, car_mileage)
    except Exception as e:
        print(f"Error scraping car data: {e}")


def insert_car_data(cursor, data):
    try:
        sql = "INSERT INTO cars (model, price, year, mileage) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, data)
    except Exception as e:
        print(f"Error inserting car data: {e}")


def main():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="kyoebrn98",
            database="cars_database",
        )
        with conn.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS cars (
                    model TEXT, 
                    price TEXT, 
                    year INT, 
                    mileage TEXT
                )"""
            )
            for i in range(1, 3):
                for car_data in scrape_car_data(browser, i):
                    insert_car_data(cursor, car_data)
                conn.commit()
    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")
    finally:
        conn.close()


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="kyoebrn98"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS cars_database")



import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="kyoebrn98",
  database = "cars_database"
)

query = "SELECT * FROM cars"

# Execute the query and load data into a Pandas DataFrame
df = pd.read_sql(query, mydb)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:kyoebrn@localhost/cars_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Welcome to your MySQL API!"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

@app.route('/get_data', methods=['GET'])
def get_data():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM your_table")
    data = cur.fetchall()
    cur.close()
    return jsonify(data)