from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

def scrape_ebay(query):
    service = Service("C:/Users/MR Segun/ShopBot/geckodriver.exe")
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(service=service, options=firefox_options)

    driver.get(f"https://www.ebay.com/sch/i.html?_nkw={query}")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    products = []

    for item in soup.select(".s-item"):
        name = item.select_one(".s-item__title").get_text() if item.select_one(".s-item__title") else "No Title"
        image = item.select_one(".s-item__image-img")
        image_url = image.get("src") if image else "No Image"
        price = item.select_one(".s-item__price").get_text() if item.select_one(".s-item__price") else "No Price"
        link = item.select_one(".s-item__link").get("href") if item.select_one(".s-item__link") else "No Link"
        rating = item.select_one(".b-starrating__star").get_text() if item.select_one(".b-starrating__star") else "No Rating"

        products.append({
            "name": name,
            "image": image_url,
            "price": price,
            "link": link,
            "rating": rating,
        })

    return products

