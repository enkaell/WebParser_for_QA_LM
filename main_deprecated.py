import bs4.element
import requests
import time
import json
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

start_time = time.time()
driver = webdriver.Chrome(ChromeDriverManager().install())

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 '
                  'Safari/537.36',
}
session = requests.Session()
target_url = "https://www.sciencedaily.com/news/computers_math/computer_science"


def write_packet(package: selenium.webdriver.remote.webelement.WebElement):
    articles = {}
    for el in package:
        driver.get(el.find_elements(By.TAG_NAME, "a")[0].get_attribute("href"))
        article = {}
        article["headline"] = driver.find_elements(By.ID, "headline")[0].text
        article["subtitle"] = driver.find_elements(By.ID, "subtitle")[0].text if driver.find_elements(By.ID,
                                                                                                      "subtitle") else None
        article["date_posted"] = driver.find_elements(By.ID, "date_posted")[0].text
        article["source"] = driver.find_elements(By.ID, "source")[0].text
        article["summary"] = driver.find_elements(By.ID, "abstract")[0].text
        article["text"] = driver.find_elements(By.ID, "text")[0].text
        articles[package.index(el)] = article
        articles
        driver.back()
        print(article)
    return articles


time.sleep(4)
if paragraph := driver.find_elements(By.ID, "summaries"):
    if articles := paragraph[0].find_elements(By.TAG_NAME, "h3"):
        res = write_packet(articles)
with open("res.json", "w") as f:
    json.dump(res, f)
    print(f"Written in file, total time: {time.time() - start_time}")
