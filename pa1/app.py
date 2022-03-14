import urllib
import urllib.request
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import concurrent.futures
import threading
import psycopg2

# 

WEB_PAGE_ADDRESS = "http://evem.gov.si"

print(f"Retrieving web page URL '{WEB_PAGE_ADDRESS}'")

request = urllib.request.Request(
    WEB_PAGE_ADDRESS, 
    headers={'User-Agent': 'fri-ieps-TEST'}
)

with urllib.request.urlopen(request) as response: 
    html = response.read().decode("utf-8")
    print(f"Retrieved Web content: \n\n'\n{html}\n'")

print('Second part')

# C:\Users\anjab\Downloads\chromedriver_win32

WEB_DRIVER_LOCATION = "/Users/anjab/Downloads/chromedriver_win32/chromedriver"
TIMEOUT = 5

chrome_options = Options()
# If you comment the following line, a browser will show ...
#chrome_options.add_argument("--headless")

#Adding a specific user agent
chrome_options.add_argument("user-agent=fri-ieps-TEST")

print(f"Retrieving web page URL '{WEB_PAGE_ADDRESS}'")
driver = webdriver.Chrome(WEB_DRIVER_LOCATION, options=chrome_options)
driver.get(WEB_PAGE_ADDRESS)

# Timeout needed for Web page to render (read more about it)
time.sleep(TIMEOUT)

html = driver.page_source

print(f"Retrieved Web content (truncated to first 900 chars): \n\n'\n{html[:900]}\n'\n")

page_msg = driver.find_element_by_class_name("inside-text")

print(f"Web page message: '{page_msg.text}'")

driver.close()

#
print('Third part')
