from html.parser import HTMLParser
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests



# Edit parameters if needed
web_driver_location = "C:\Users\anjab\Downloads\chromedriver_win32\chromedriver"
user_agent = "user-agent=fri-ieps-OSKAR"
timeout = 3

# Options (do not edit)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(user_agent)
driver = webdriver.Chrome(web_driver_location, options=chrome_options)



# Crawl page
def crawl_page(url):
    driver.get(url)
    time.sleep(timeout) # waiting for page to load

    html = driver.page_source
    page_msg = driver.find_element_by_class_name("inside-text")

    button = driver.find_elements_by_xpath("//button[@onclick]")
    code = driver.find_elements_by_xpath("//script")
    elems = driver.find_elements_by_xpath("//a[@href]")
    # add method for parsing each of the above three



#GET DATA_TYPE FROM URL
def get_type (url):
    data = requests.head(url)
    header = data.headers
    data_type = header.get('Content-Type')

    return data_type


# Class link finder for parsing sitemap _ WONT WORK - need to parse XML site (not necesarilly)
# Preveri kak hmtl parsa xml - če se da s tem
class LinkFinder(HTMLParser):

    def __init__(self, page_url):
        super().__init__()
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = urljoin(self.page_url, value)
                    self.links.add(url)

    def page_links(self):
        return self.links

    def error(self, message):
        pass
