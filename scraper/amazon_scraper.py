from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

def scrape_amazon(query):
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")
    service = Service("C:/Users/MR Segun/ShopBot/geckodriver.exe")  # Update with your ChromeDriver path

    driver = webdriver.Chrome(service=service, options=firefox_options)
    url = f"https://www.amazon.com/s?k={query}"
    driver.get(url)
    time.sleep(3)  # Wait for the page to load
    
    products = []
    
    items = driver.find_elements(By.CSS_SELECTOR, ".s-main-slot .s-result-item")
    for item in items:
        try:
            name = item.find_element(By.CSS_SELECTOR, "span.a-text-normal").text
            price = item.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
            link = item.find_element(By.CSS_SELECTOR, "a.a-link-normal").get_attribute("href")
            image = item.find_element(By.CSS_SELECTOR, "img.s-image").get_attribute("src")
            rating = item.find_element(By.CSS_SELECTOR, "span.a-icon-alt").text
            
            products.append({
                "name": name,
                "price": price,
                "link": link,
                "image": image,
                "rating": rating
            })
        except Exception as e:
            continue
    
    driver.quit()
    return products
