from html.parser import HTMLParser
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests

import db
import main
import general


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

    response = requests.get(url)
    status = response.status_code

    a_corrected = general.correct_url(url)
    a_cannonical = general.url_canonical(url)
    domain = general.domain_name(url)
    IP = general.get_ip_address(domain)

    data_ytpe = get_type(url)
    
    robots_content = general.get_robots_txt('https://'+domain)
    #robots_info = general.get_robots_info(robots_content[1])  


    links_h = driver.find_elements_by_tag_name("a")
    links_i = driver.find_elements_by_tag_name("img")
    links_b = driver.find_elements_by_xpath("//button[@onclick]")
    for link_h in links_h:
        link_h = link_h.get_attribute('href')
        if 'gov.si' in link_h:
           print(link_h) #ADD TO FRONTIER
    for link_i in links_i:
        link_i = link_i.get_attribute('src')
        if 'gov.si' in link_i:
           print(link_i) #ADD TO FRONTIER
    for link_b in links_b:        
        link_b = link_b.get_attribute('onclick') 
        if 'gov.si' in link_b:
            print(link_b) #ADD TO FRONTIER
    driver.quit()      
    #ADD LINKS TO FRONTIER!!!!!!!!  
    # if url in db
    # don't add!!!


    #html = driver.page_source
    #page_msg = driver.find_element_by_class_name("inside-text")
    #code = driver.find_elements_by_xpath("//script")
    #elems = driver.find_elements_by_xpath("//a[@href]")
    # add method for parsing each of the above three



#GET DATA_TYPE FROM URL
def get_type (url):
    data = requests.head(url)
    header = data.headers
    data_type = header.get('Content-Type')

    return data_type


#STATUS CODE
def status_code (url):
    response = requests.get(url)
    status = response.staut_code

    return status_code

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
