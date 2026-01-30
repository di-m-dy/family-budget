"""
Module for utility functions for the parser package.
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


def parse_invoice(url: str) -> dict:
    """
    Parse invoice data from a given URL using Selenium and BeautifulSoup.
    """
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "invoice-amount")))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        invoice_amount = soup.find("div", class_="invoice-amount")
        invoice_place = soup.find("li", class_="invoice-basic-info--business-name")
        invoice_address = soup.find("li", class_="invoice-basic-info--business-address")
        invoice_date = soup.find("li", class_="invoice-basic-info--date")
        invoice_items = soup.find(class_="invoice-items")
        driver.quit()

        result = {}

        if invoice_amount:
            result["amount"] = (
                invoice_amount.find("h1").find("strong").get_text().strip()
            )
        if invoice_place:
            result["place"] = invoice_place.get_text().strip()
        if invoice_address:
            result["address"] = invoice_address.get_text().strip()
        if invoice_date:
            result["date"] = invoice_date.get_text().strip()

        if invoice_items:
            items = []
            for item in invoice_items.find_all("li", class_="invoice-item"):
                title = item.find("span", class_="invoice-item--title").get_text()
                price = item.find("span", class_="invoice-item--price").get_text()
                items.append({"title": title, "price": price})
            result["items"] = items
        return result
    except Exception as e:
        driver.quit()
        raise e
