from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

def scrape_jumia(query):
    service = Service("C:/Users/MR Segun/ShopBot/geckodriver.exe")  # Update with the correct path to geckodriver
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Firefox(service=service, options=firefox_options)

    driver.get(f"https://www.jumia.com.ng/catalog/?q={query}")

    try:
        # Wait for the products grid to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".c-prd"))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        products = []

        for item in soup.select(".c-prd"):
            name = item.select_one(".name").get_text() if item.select_one(".name") else "No Title"
            image = item.select_one("img").get("data-src") if item.select_one("img") else "No Image"
            price = item.select_one(".prc").get_text() if item.select_one(".prc") else "No Price"
            link = item.select_one("a").get("href") if item.select_one("a") else "No Link"
            rating = item.select_one(".stars._s").get_text() if item.select_one(".stars._s") else "No Rating"

            products.append({
                "name": name,
                "image": image,
                "price": price,
                "link": f"https://www.jumia.com.ng{link}",
                "rating": rating,
            })

        return products

    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()
        return []

