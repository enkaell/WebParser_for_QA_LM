import bs4.element
import requests
import time
import json
from bs4 import BeautifulSoup
import logging
import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

path = os.getcwd() + "/datasets"
os.chdir(path)

logging.basicConfig(level=logging.INFO, filename='webparser.log')

all_categories = ["nanotech-news", "earth-news", "space-news", "chemistry-news", "biology-news",
                  "science-news"]
start_time = time.time()
session = requests.Session()
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 '
                  'Safari/537.36',
}


def get_one_package(package: bs4.element.ResultSet, page_number: int) -> dict():
    articles = dict()
    for el in package:
        article = {}
        driver.get(el.findChild("a", {"class": "news-link"}).attrs.get("href"))
        driver.find_elements(By.CLASS_NAME, "text-extra-large line-low mb-2")
        article["header"] = soup.find('h1', {"class": "text-extra-large line-low mb-2"}).text
        article["author"] = soup.find("p", {"class": "article-byline text-low"}).text
        article["text"] = [i.text for i in soup.find("div", {"class": "mt-4 article-main"}).findAll("p")]
        articles[package.index(el) + 1 + page_number * 10] = article
    return articles


for categorie in all_categories:
    req = session.get(f"https://phys.org/{categorie}/sort/date/all/", headers=headers)
    if req.status_code != 200:
        logging.info("Error status code ", req.status_code)
        time.sleep(30)
        req = session.get(f"https://phys.org/{categorie}/sort/date/all/", headers=headers)
    count_of_pages = int(BeautifulSoup(req.text, 'html.parser').find("div", "pagination-view mr-4").find("span").text)
    for page in range(count_of_pages):
        res = session.get(f"https://phys.org/physics-news/sort/date/all/page{page}.html", headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        package = soup.findAll("article", {"class": "sorted-article"})
        with open(f"{categorie}.json", "a+") as f:
            f.write(json.dumps(get_one_package(package, page_number=page)))
    print(f"Written in file {categorie}.json")
