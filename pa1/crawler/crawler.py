from hashlib import new
from urllib.parse import urljoin
from attr import validate
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import datetime
from urllib.parse import urldefrag

from db import *
from general import *


# Edit parameters if needed
web_driver_location = "C:/Users/anjab/Downloads/chromedriver_win32/chromedriver"
user_agent = "user-agent=fri-ieps-OSKAR"
timeout = 4

# Options (do not edit)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(user_agent)
driver = webdriver.Chrome(executable_path=web_driver_location, options=chrome_options)



# Crawl page
def crawl_page(url, crawl_delay, site_id):

    if url.startswith('www'):
        url = 'http://'+url
    else:
        url = 'http://www.'
    #crawl_delay, site_id = db.get_crawl_delay_siteid(domain_name(url))

    try:
        time.sleep(crawl_delay+1)
        response = requests.head(url, allow_redirects=True, timeout=2)
        http_status_code = response.status_code
        page_type_code_raw = response.headers['content-type']
        page_type_code = get_content_type(page_type_code_raw)
        accessed_time = datetime.datetime.now() # with HTML we'll override it
        last_accessed_time = int(time.time()) # with HTML we'll override it

    except Exception as e:
        print("Request head failed :", e)

        try:

            time.sleep(crawl_delay+1)
            response = requests.get(url, allow_redirects=True, timeout=4)
            http_status_code = response.status_code
            page_type_code_raw = response.headers['content-type']
            page_type_code = get_content_type(page_type_code_raw)
            accessed_time = datetime.datetime.now() # with HTML we'll override it
            last_accessed_time = int(time.time()) # with HTML we'll override it

        except:

            time.sleep(crawl_delay*2)
            response = requests.get(url, allow_redirects=True, timeout=4)
            http_status_code = response.status_code
            page_type_code_raw = response.headers['content-type']
            page_type_code = get_content_type(page_type_code_raw)
            accessed_time = datetime.datetime.now() # with HTML we'll override it
            last_accessed_time = int(time.time()) # with HTML we'll override it
    


    # Content type HTML
    if page_type_code == 'HTML':

        time.sleep(crawl_delay)
        driver.get(url)
        time.sleep(timeout) # waiting for page to load

        html_content = driver.page_source

        accessed_time = datetime.datetime.now()
        last_accessed_time = int(time.time())
        hash = html_hash(html_content)

        # Update page in database
        write_url = check_potential_url(url)
        db.update_page(site_id, page_type_code, write_url, html_content, http_status_code, accessed_time, hash, last_accessed_time)

        # get URLs and site_ids from page
        new_urls, site_ids, number = get_urls(driver)

        try: 
            write_url_to_frontier(number, new_urls, site_ids)
        except:
            print('ERROR getting urls to db')
    

        try:
            # IMAGES
            for link in driver.find_elements_by_tag_name("img"):
                image_links = []
                l = link.get_attribute('src')
                if 'gov.si' in l:
                    image_links.append(l)
                    
            new_urls, site_ids, number = clean_urls(image_links)
            write_url = check_potential_url(new_urls)


            accessed_time = datetime.datetime.now()
            page_type_code = 'BINARY'
            content_type = 'image'

            db.write_img(number, write_url, site_ids, page_type_code, content_type, accessed_time)
        except:
            pass

        # BINARY page_data
        # Types: https://www.iana.org/assignments/media-types/media-types.xhtml
        else:
            if 'application/pdf' in page_type_code_raw:
                page_data_type = 'PDF'
                ## page.id
                ## site_id
                # page_type_code
                # url
                ## html_content = none
                # http_status_code
                # accessed_time
                # last_accessed_time

            if 'application/msword' in page_type_code_raw:
                page_data_type = 'DOC'

            if 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in page_type_code_raw:
                page_data_type = 'DOCX'


            if 'application/vnd.ms-powerpoint' in page_type_code_raw:
                page_data_type = 'PPT'

            if 'application/vnd.openxmlformats-officedocument.presentationml.presentation' in page_type_code_raw:
                page_data_type = 'PPTX'

            try:

                write_url = check_potential_url(url)
                db.write_data(page_type_code, write_url, http_status_code, accessed_time, last_accessed_time, page_data_type)
            except:
                pass
            


def get_urls(driver):
    possible_urls = []

    links_h = driver.find_elements_by_tag_name("a")
    links_b = driver.find_elements_by_xpath("//button[@onclick]")
    links_s = driver.find_elements_by_xpath("//script")

    for link in links_h:
        try:
            l = link.get_attribute('href')
            if '.gov.si' in l:
                possible_urls.append(l)
        except:
            pass

    for link in links_b:
        try:
            l = link.get_attribute('onclick')
            if '.gov.si' in l:
                possible_urls.append(l)
        except:
            pass

    for link in links_s:
        try:
            l = link.get_attribute("innerText")
            if '.gov.si' in l:
                possible_urls.append(l)
        except:
            pass

    new_urls, site_ids, number = clean_urls(possible_urls)

    return new_urls, site_ids, number



def clean_urls(possible_urls):
    new_urls = []
    site_ids = []
    number = 0

    for url in possible_urls:
        

        if "javascript" in url.lower():
            continue
        if url.startswith("mailto"):
            continue


        url = urldefrag(url)[0]
        #url = url_canonical(url)

        if url.endswith("/"):
            url = url[:-1]

        if url.endswith("/index.html"):
            url = url[:-11]

        if url.endswith("/index.php"):
            url = url[:-10]

        
        validated_url = check_potential_url(url)

        if validated_url == -1:
            continue

        domain, site_id, disallow = domain_name_new(validated_url)

        #for disa in disallow:
            #if disa not in url:
               # continue

        new_urls.append(validated_url)
        site_ids.append(site_id)
        number = number + 1

    return new_urls, site_ids, number
