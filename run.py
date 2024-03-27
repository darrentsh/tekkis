from main import scrape_cars
from api import API

if __name__ == "__main__":
    # scrape_cars(1, 4)
    api = API()
    api.app.run(debug=True, use_reloader=False, port=9874)
