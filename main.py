from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import sys
import time
import requests
import datetime 
from datetime import date
import pandas as pd

########################################################################
Expiry = "2022-04-13"   
symbol_prefix = "BANKNIFTY22413"	
total_capital = 21285
########################################################################
api = "ENTER YOUR API"
user_id = "ENTER YOUR USER ID"
password = "ENTER YOU LOGIN PASSWORD"
passcode = int(input())
########################################################################
logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key=api)
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(r'chromedriver.exe', options=chrome_options)
driver.get(f"https://kite.zerodha.com/connect/login?v=3&api_key={api}")
driver.implicitly_wait(10)
driver.find_element_by_xpath('//*[@id="userid"]').send_keys(user_id)
driver.implicitly_wait(10)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
driver.implicitly_wait(10)
driver.find_element_by_xpath('//*[@id="container"]/div/div/div[2]/form/div[4]/button').click()
driver.implicitly_wait(10)
driver.find_element_by_xpath('//*[@id="totp"]').send_keys(passcode)
driver.implicitly_wait(10)
driver.find_element_by_xpath('//*[@id="container"]/div/div/div[2]/form/div[3]/button').click()
time.sleep(5)
final_url = driver.current_url
try:
  request_token = str(final_url.split("request_token=")[1].split('&action')[0])
except:
  request_token = str(final_url.split("request_token=")[1])
data = kite.generate_session(request_token, api_secret="owb9i3fpb9tcaw8abj7zck7tvryzuihg")
kite.set_access_token(data["access_token"])
