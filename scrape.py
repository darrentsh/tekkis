import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


class Scrape:

    def find_word_before_decimal(self, text):
        pattern = re.compile(r"\d+\.\d+")
        match = pattern.search(text)
        if match:
            index_a = match.start()
            word_before_a = text[: index_a + 3]
            return word_before_a
        else:
            return text

    def scrape_car_data(self, browser, page_num):
        car_data = []
        try:
            browser.get(f"https://www.mudah.my/malaysia/cars-for-sale?o={page_num}")
            wait = WebDriverWait(browser, 10)
            car_list = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, '[data-testid^="listing-ad-item-"]')
                )
            )
            time.sleep(5)
            for car in car_list:

                car_price = re.findall(re.compile("RM \d+,\d+"), car.text)[0]
                try:
                    car_year = car.find_element(
                        By.CSS_SELECTOR, '[title="Manufactured Year"]'
                    ).get_attribute("innerText")
                except NoSuchElementException:
                    car_year = car.find_element(
                        By.CSS_SELECTOR, '[data-testid="year-verified-badge"]'
                    ).get_attribute("innerText")

                car_brand_model = self.find_word_before_decimal(
                    car.find_element(By.TAG_NAME, "a")
                    .get_attribute("title")
                    .replace(f"{car_year} ", "")
                )

                car_mileage = car.find_element(
                    By.CSS_SELECTOR, '[title="Mileage"]'
                ).get_attribute("innerText")
                car_data.append((car_brand_model, car_price, car_year, car_mileage))

            return car_data

        except Exception as e:
            print(f"Error scraping car data: {e}")
