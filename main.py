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
total_capital = 21285 #Caplital you want to trade this stratrgy
qty = 50 # trade quantity
########################################################################
api = "ENTER YOUR API"
user_id = "ENTER YOUR USER ID"
password = "ENTER YOU LOGIN PASSWORD"
passcode = int(input("ENter TOTP "))
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


url = 'https://api.kite.trade/instruments'
r = requests.get(url)
open('Script.csv', 'wb').write(r.content)

df = pd.read_csv('Script.csv')
df_script = df.dropna()
df_script = df_script[df_script['name'].str.contains('BANKNIFTY')]
df_script = df_script[df_script['expiry'].str.contains(Expiry)]
df_script = df_script[df_script.instrument_type != 'FUT']
tokens = df_script['instrument_token'].to_numpy()
df_fut_token = df[df['tradingsymbol'].str.contains('NIFTY BANK')]['instrument_token'].to_numpy()

looping_entry = False
looping_exit = False

while not looping_entry:
    current_time = datetime.datetime.now() 
    now = current_time.strftime("%H:%M:%S")
    if (now == '09:20:00'):
        bn_current_price = kite.quote(df_fut_token[0])
        bn_price = list(bn_current_price.items())[0][1]['last_price']
        strike = int(round(bn_price / 100.0)) * 100
        trade_symbol_1 =symbol_prefix+str(strike)+'CE'
        trade_symbol_2 =symbol_prefix+str(strike)+'PE'
        print(trade_symbol_1)
        print(trade_symbol_2)
        

        try:
            order_id_1 = kite.place_order(variety=kite.VARIETY_REGULAR,
                                        tradingsymbol=trade_symbol_1,
                                        exchange=kite.EXCHANGE_NFO,
                                        transaction_type=kite.TRANSACTION_TYPE_SELL,
                                        quantity=qty,
                                        order_type=kite.ORDER_TYPE_MARKET,
                                        product=kite.PRODUCT_NRML)
            order_id_2 = kite.place_order(variety=kite.VARIETY_REGULAR,
                                        tradingsymbol=trade_symbol_2,
                                        exchange=kite.EXCHANGE_NFO,
                                        transaction_type=kite.TRANSACTION_TYPE_SELL,
                                        quantity=qty,
                                        order_type=kite.ORDER_TYPE_MARKET,
                                        product=kite.PRODUCT_NRML)

            logging.info("Order placed. ID is: {}".format(order_id_1))
            logging.info("Order placed. ID is: {}".format(trade_symbol_2))
            looping_entry =True
        except Exception as e:
            logging.info("Order placement failed: {}".format(e.message))
            looping_entry =True
            looping_exit = True
    
      
while not looping_exit:
    current_time = datetime.datetime.now() 
    now = current_time.strftime("%H:%M:%S")
    if (now == '15:00:00'):
      try:
        order_id_1 = kite.place_order(variety=kite.VARIETY_REGULAR,
                                    tradingsymbol=trade_symbol_1,
                                    exchange=kite.EXCHANGE_NFO,
                                    transaction_type=kite.TRANSACTION_TYPE_BUY,
                                    quantity=qty,
                                    order_type=kite.ORDER_TYPE_MARKET,
                                    product=kite.PRODUCT_NRML)
        logging.info("Order placed. ID is: {}".format(order_id_1))
        order_id_2 = kite.place_order(variety=kite.VARIETY_REGULAR,
                                    tradingsymbol=trade_symbol_2,
                                    exchange=kite.EXCHANGE_NFO,
                                    transaction_type=kite.TRANSACTION_TYPE_BUY,
                                    quantity=qty,
                                    order_type=kite.ORDER_TYPE_MARKET,
                                    product=kite.PRODUCT_NRML)
        logging.info("Order placed. ID is: {}".format(order_id_2))
        looping_exit = True
      except Exception as e:
          logging.info("Order placement failed: {}".format(e.message))
          looping_exit = True
