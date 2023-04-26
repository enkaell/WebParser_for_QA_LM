import bs4.element
import requests
import time
import json
from bs4 import BeautifulSoup
import logging
import os

path = os.getcwd() + "/datasets"
os.chdir(path)


def json_cleaning(path: str) -> None:
    files_list = [filename for filename in os.listdir(path) if ".json" in filename]
    for file in files_list:
        with open(file, "w+") as f:
            for ch in f:
                if ch == "\n" or ch == "\t":
                    print(ch)
        f.close()


json_cleaning(path)
