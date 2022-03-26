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
timeout = 10
headers = {'User-Agent': 'fri-ieps-OSKAR'}

# Options (do not edit)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(user_agent)
driver = webdriver.Chrome(executable_path=web_driver_location, options=chrome_options)



# Crawl page
def crawl_page(thread_name, url, crawl_delay, site_id):

    #global page_type_code
    global page_type_code_raw
    page_type_code_raw = ''
    page_type_code = ''

    print(thread_name + ' crawling ' + url)

    if url.startswith('www'):
        url_req = 'http://'+ url
    else:
        url_req = url
 
    try:
        #time.sleep(crawl_delay)
        response = requests.head(url_req, allow_redirects=True, timeout=timeout, headers=headers)
        http_status_code = response.status_code
        page_type_code_raw = response.headers['content-type']
        page_type_code = get_content_type(page_type_code_raw)
        last_accessed_time = int(time.time())
        print("craw_page request.head successful", page_type_code)
        db.update_last_accessed_time(site_id, last_accessed_time)

    except Exception as e:
        print("Request head failed :", e)
        
        try:

            time.sleep(crawl_delay)
            response = requests.get(url_req, allow_redirects=True, timeout=timeout, headers=headers)
            http_status_code = response.status_code
            page_type_code_raw = response.headers['content-type']
            page_type_code = get_content_type(page_type_code_raw)
            last_accessed_time = int(time.time())
            print("craw_page request.get successful", page_type_code)
            db.update_last_accessed_time(site_id, last_accessed_time)


        except Exception as e:
            print(e)
            print("crawl_page request failed)")
            last_accessed_time = int(time.time())
            page_type_code_raw = ''
            page_type_code = ''
            db.update_last_accessed_time(site_id, last_accessed_time)

        
            #try:
         #      http_status_code = response.status_code
          #  except:
          #      http_status_code = 0 # Hardcode - zbriši

           # try:
          #      page_type_code_raw = response.headers['content-type']
          #      page_type_code = get_content_type(page_type_code_raw)
           # except:
          #      page_type_code = ''
         #       page_type_code_raw = ''
            
          #  accessed_time = datetime.datetime.now()
          #  hash = 0
          #  last_accessed_time = int(time.time())
          #  html_content = 0

    print(page_type_code_raw, page_type_code)
    # Content type HTML
    if page_type_code == 'HTML':

        time.sleep(crawl_delay)
        driver.get(url_req)
        time.sleep(timeout) # waiting for page to load

        html_content = driver.page_source

        accessed_time = datetime.datetime.now()
        last_accessed_time = int(time.time())
        hash = html_hash(html_content)

        # Update page in database
        db.update_page(site_id, page_type_code, url, html_content, http_status_code, accessed_time, hash, last_accessed_time)
        print("Page updated in db: ", url)

        # get URLs and site_ids from page
        new_urls, site_ids, number = get_urls(driver)

        if number >= 1: 
            write_url_to_frontier(number, new_urls, site_ids, url)
        

        # BINARY page_data
        # Types: https://www.iana.org/assignments/media-types/media-types.xhtml
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
    elif page_type_code == 'BINARY':

        if 'application/pdf' in page_type_code_raw:
            page_data_type = 'PDF'
            print(page_data_type)
            print(page_type_code)
            
            db.write_data(page_type_code, url, http_status_code, accessed_time, page_data_type)


        if 'application/msword' in page_type_code_raw:
            page_data_type = 'DOC'
            print(page_data_type)
            print(page_type_code)

            db.write_data(page_type_code, url, http_status_code, accessed_time, page_data_type)


        if 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or 'application/octet-stream' in page_type_code_raw:
            page_data_type = 'DOCX'
            print(page_data_type)
            print(page_type_code)

            db.write_data(page_type_code, url, http_status_code, accessed_time, page_data_type)


        if 'application/vnd.ms-powerpoint' in page_type_code_raw:
            page_data_type = 'PPT'
            print(page_data_type)
            print(page_type_code)

            db.write_data(page_type_code, url, http_status_code, accessed_time, page_data_type)


        if 'application/vnd.openxmlformats-officedocument.presentationml.presentation' in page_type_code_raw:
            page_data_type = 'PPTX'
            print(page_data_type)
            print(page_type_code)

            db.write_data(page_type_code, url, http_status_code, accessed_time, page_data_type)

            
        if 'image' in page_type_code_raw:
            content_type = page_type_code_raw
            print(page_type_code)
            print(content_type)

            db.write_img(url, site_id, page_type_code, content_type, accessed_time)



def get_urls(driver):
    possible_urls = []

    links_h = driver.find_elements_by_tag_name("a")
    links_b = driver.find_elements_by_xpath("//button[@onclick]")
    #links_s = driver.find_elements_by_xpath("//script")
    links_i=  driver.find_elements_by_tag_name("img")
        

    for link in links_h:
        try:
            l = link.get_attribute('href')
            if '.gov.si' in domain_name(l): # Added domain_name so we don't get other (not gov.si) pages contining gov.si
                possible_urls.append(l)
        except:
            pass

    for link in links_b:
        try:
            l = link.get_attribute('onclick')
            if '.gov.si' in domain_name(l):
                possible_urls.append(l)
        except:
            pass

    #for link in links_s:
        #try:
            #l = link.get_attribute("innerText")
            #if '.gov.si' in domain_name(l):
                #possible_urls.append(l)
        #except:
            #pass

    for link in links_i:
        try:
            l = link.get_attribute('src')
            if 'gov.si' in domain_name(l):
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

        if validated_url.endswith(".zip"): # We dont handle zip files
            validated_url = -1

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
