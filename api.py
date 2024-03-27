from flask import Flask, jsonify, request
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
import pandas as pd


class API:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="kyoebrn98",
            database="cars_database",
        )
        self.cursor = self.conn.cursor(dictionary=True)

        self.app = Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = (
            "mysql+pymysql://root:kyoebrn98@localhost/cars_database"
        )
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.db = SQLAlchemy(self.app)

        @self.app.route("/")
        def index():
            return "Welcome to your MySQL API!"

        @self.app.route("/cars", methods=["GET"])
        def get_cars():
            try:
                self.cursor.execute("SELECT * FROM cars")
                cars = self.cursor.fetchall()
                return jsonify(cars)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/cars/<int:car_id>", methods=["GET"])
        def get_car(car_id):
            try:
                self.cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
                car = self.cursor.fetchone()
                if car:
                    return jsonify(car)
                else:
                    return jsonify({"message": "Car not found"}), 404
            except Exception as e:
                return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    api = API()
    api.app.run(debug=True, use_reloader=False, port=9874)
