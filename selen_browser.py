from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def open_page(url):
    # using selenium web for navigation
    chrome_options = Options()

    chrome_options.add_argument('--headless')

    # block all website notification
    chrome_options.add_argument('--disable-notifications')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

    driver.maximize_window()
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source,'html.parser')

    driver.quit()

    return soup

