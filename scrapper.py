import bs4.element
import requests
import time
import json
from bs4 import BeautifulSoup
import logging
import os
import urllib3
import asyncio
import aiohttp

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

path = os.getcwd() + "/datasets"
os.chdir(path)

logging.basicConfig(level=logging.INFO, filename='webparser.log')

start_time = time.time()
session = requests.Session()


class WebScrapper(object):
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 '
                          'Safari/537.36',
        }
        self.path = os.getcwd() + "/datasets"
        self.all_categories = ["physics-news", "nanotech-news", "earth-news", "space-news", "chemistry-news", "biology-news",
                               "science-news"]
        self.start_time = time.time()
        os.chdir(path)
        logging.basicConfig(level=logging.INFO, filename='webparser.log')
        self.main()

    def get_one_package(self, package: bs4.element.ResultSet, page_number: int) -> dict():
        articles = dict()
        for el in package:
            time.sleep(0.3)
            article = {}
            target_url = el.findChild("a", {"class": "news-link"}).attrs.get("href")
            res = session.get(target_url, headers=self.headers)
            if res.status_code != 200:
                logging.error(f"HTTP status code {res.status_code} at {time.time() - start_time}")
                time.sleep(60)
                res = session.get(target_url, headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            article["header"] = soup.find('h1', {"class": "text-extra-large line-low mb-2"}).text + "\n"
            article["author"] = soup.find("p", {"class": "article-byline text-low"}).text + "\n"
            article["date"] = soup.find("p", {"class": "text-uppercase text-low"}).text + "\n"
            article["text"] = [i.text for i in soup.find("div", {"class": "mt-4 article-main"}).findAll("p")][0] + "\n"
            articles[package.index(el) + 1 + page_number * 10] = article
        return articles

    def get_one_page(self, page: str, categorie: str) -> dict:
        time.sleep(0.5)
        res = session.get(f"https://phys.org/{categorie}/sort/date/all/page{page}.html", headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        package = soup.findAll("article", {"class": "sorted-article"})
        return self.get_one_package(package, page)

    def main(self):
        for categorie in self.all_categories:
            time.sleep(0.3)
            categorie_dict = {}
            req = session.get(f"https://phys.org/{categorie}/sort/date/all/", headers=self.headers, verify=False,
                              timeout=5)
            if req.status_code != 200:
                logging.info(f"Error status code {req.status_code}")
                time.sleep(30)
                req = session.get(f"https://phys.org/{categorie}/sort/date/all/", headers=self.headers)
            count_of_pages = int(
                BeautifulSoup(req.text, 'html.parser').find("div", "pagination-view mr-4").find("span").text)
            for page in range(count_of_pages):
                categorie_dict[page+1] = self.get_one_page(page=page, categorie=categorie)
            with open(f"{categorie}.json", "a+") as f:
                json.dump(categorie_dict, f, indent=1)
        print(f"Finished in {time.time() - self.start_time}")


scrapper = WebScrapper()
