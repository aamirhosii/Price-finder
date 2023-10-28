from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import List
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_product_price(urls: List[str], product_name):
    dict = {}
    safari_options = webdriver.SafariOptions()
    safari_options.add_argument('--disable-notifications')
    for url in urls:
        driver = webdriver.Safari(options=safari_options)

        driver.get(url)
        search_bar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "HeaderSearch_search_query")))
        if search_bar is None:
            search_bar = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "mobile-search-bar"))
            )

        search_bar.send_keys(product_name)
        button = driver.find_element(By.XPATH, "//button[@aria-label='Search submit']")
        button.click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                   "ProductCard-link")))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        price = soup.find("span", class_="ProductPrice")
        price = price.text.strip()
        driver.quit()
        dict[url] = price
    return dict

urls = ["https://www.footlocker.ca"]
print(get_product_price(urls, "Jordan Retro 1 Low SE"))
