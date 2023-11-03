# Libraries

from chat_downloader import ChatDownloader
import requests as req
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import json
import datetime


from pymongo import MongoClient
from passwords import STR_CONN # a file with my connection string to the mongodb atlas db

from pysentimiento import create_analyzer

import pandas as pd

# Driver options

opciones=Options()

opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
opciones.add_experimental_option('useAutomationExtension', False)
opciones.headless=False
opciones.add_argument('--start-maximized')
opciones.add_argument('--incognito')

while True:
    try:
        # code
    except:
        break