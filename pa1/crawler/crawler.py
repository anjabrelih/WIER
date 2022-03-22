from url_normalize import url_normalize
from urllib.parse import urlparse
from urllib.parse import urldefrag
from html.parser import HTMLParser
from urllib.parse import urljoin
import urllib.request
import io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import robotexclusionrulesparser
import socket
import time
import urllib.robotparser


# Edit parameters if needed
web_driver_location = "C:\Users\anjab\Desktop\MSc_MM\FRI_Iskanje in ekstrakcija podatkov s spleta\Vaje\WIER\pa1\chromedriver"
user_agent = "user-agent=fri-ieps-OSKAR"
timeout = 3

# Options (do not edit)
robotex = robotexclusionrulesparser.RobotExclusionRulesParser()
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




# Correct url (before canonicalization!)
def correct_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
        
    return url


# URL canonicalization
def url_canonical(url):
    parse_url = urlparse(correct_url(url))
    url_can = parse_url.scheme + "://" + parse_url.netloc + parse_url.path
    url_can_norm = url_normalize(url_can)

    return url_can_norm

# Get robots.txt content
def get_robots_txt(domain_url):
    if domain_url.endswith('/'):
        path = domain_url
    else:
        path = domain_url + '/'
    req = urllib.request.urlopen(path + "robots.txt", data=None)
    data = io.TextIOWrapper(req, encoding='utf-8')

    return data.read()


<<<<<<< HEAD
##################################
#NEW FUNCTION FOR CRAWL DELAY!!!!
##################################
def get_Delay_Sitemaps(url):
    url_r = urljoin(url,'/robots.txt')
    rb = urllib.robotparser.RobotFileParser(url_r)
    user_agent = "*"
    rb.set_url(url_r)
    rb.read()
    rb.can_fetch(user_agent,url_r)
    delay = rb.crawl_delay(user_agent)
    sitemaps = rb.site_maps()

    return delay, sitemaps




# Get domain name
=======
# Get (sub)domain name
>>>>>>> bd79df5aa4f14b643410a6b7abfcfae01e223c30
def domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''


# Get domain IP address
def get_ip_address(url):
    try:
        return socket.gethostbyname(url)
    except:
        return ''


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
