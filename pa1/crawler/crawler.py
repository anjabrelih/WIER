from hashlib import new
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import datetime
from urllib.parse import urldefrag

import db
import general


# Edit parameters if needed
web_driver_location = "C:/Users/anjab/Downloads/chromedriver_win32/chromedriver"
user_agent = "user-agent=fri-ieps-OSKAR"
timeout = 3

# Options (do not edit)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(user_agent)
driver = webdriver.Chrome(executable_path=web_driver_location, options=chrome_options)



# Crawl page
def crawl_page(url):

    crawl_delay, site_id = db.get_crawl_delay(general.domain_name(url))

    try:
        response = requests.head(url, allow_redirects=True, timeout=timeout)
        http_status_code = response.status_code
        page_type_code_raw = response.headers['content-type']
        page_type_code = general.get_content_type(page_type_code_raw)
        time.sleep(crawl_delay)

    except Exception as e:
        print("Request head failed :", e)

        response = requests.get(url, allow_redirects=True, timeout=4)
        http_status_code = response.status_code
        page_type_code_raw = response.headers['content-type']
        page_type_code = general.get_content_type(page_type_code_raw)
        time.sleep(crawl_delay)


    # Content type HTML
    if page_type_code == 'HTML':

        driver.get(url)
        time.sleep(timeout) # waiting for page to load

        html_content = driver.page_source

        accessed_time = datetime.datetime.now()
        last_accessed_time = int(time.time())
        hash = general.html_hash(html_content)

        # Update page in database
        db.update_page(site_id, page_type_code, url, html_content, http_status_code, accessed_time, hash, last_accessed_time)

        # get URLs and site_ids from page
        new_urls = get_urls(driver)

    
    


def get_urls(driver):
    possible_urls = []

    links_h = driver.find_elements_by_tag_name("a")
    links_i = driver.find_elements_by_tag_name("img")
    links_b = driver.find_elements_by_xpath("//button[@onclick]")
    links_s = driver.find_elements_by_xpath("//script")

    for link in links_h:
        try:
            l = link.get_attribute('href')
            if 'gov.si' in l:
                possible_urls.append(l)
        except:
            pass
    
    for link in links_i:
        try:
            l = link.get_attribute('src')
            if 'gov.si' in l:
                possible_urls.append(l)
        except:
            pass

    for link in links_b:
        try:
            l = link.get_attribute('onclick')
            if 'gov.si' in l:
                possible_urls.append(l)
        except:
            pass

    for link in links_s:
        try:
            l = link.get_attribute("innerText")
            if 'gov.si' in l:
                possible_urls.append(l)
        except:
            pass

    newurls_siteid = clean_urls(possible_urls)

    return newurls_siteid



def clean_urls(possible_urls):
    newurls_siteid = []

    for url in possible_urls:
        if "javascript" in url.lower():
            continue

        url = urldefrag(url)[0]
        url = general.url_canonical(url)

        if url.endwith("/"):
            url = url[:-1]

        if url.endwith("/index.html"):
            url = url[:-11]

        if url.endwith("/index.php"):
            url = url[:-10]

        
        domain, site_id, disallow = general.domain_name(url)

        for disa in disallow:
            if disa not in url:
                continue

        newurls_siteid.append(url, site_id)

    return newurls_siteid
