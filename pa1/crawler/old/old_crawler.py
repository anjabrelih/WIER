from hashlib import new
from urllib.parse import urljoin
from attr import validate
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import datetime
from urllib.parse import urldefrag

from old_db import *
from old_general import *


# Edit parameters if needed
web_driver_location = "C:/Users/anjab/Downloads/chromedriver_win32/chromedriver"
user_agent = "user-agent=fri-ieps-OSKAR"
timeout = 5
headers = {'User-Agent': 'fri-ieps-OSKAR'}

# Options (do not edit)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(user_agent)
chrome_options.add_argument('ignore-certificate-errors')
driver = webdriver.Chrome(executable_path=web_driver_location, options=chrome_options)



# Crawl page
def crawl_page(thread_name, page, conn):

    #global page_type_code
    #global page_type_code_raw
    page.page_type_code_raw = ''
    page.page_type_code = ''

    print(thread_name + ' crawling ' + page.url)

    if page.url.startswith('www'):
        page.url_req = 'http://'+ page.url
    else:
        page.url_req = page.url
 
    try:
        #time.sleep(crawl_delay)
        page.last_accessed_time = int(time.time())
        db.update_last_accessed_time(page.site_id, page.last_accessed_time, conn)
        response = requests.head(page.url_req, allow_redirects=True, timeout=timeout, headers=headers, verify=False)
        page.http_status_code = response.status_code
        page.page_type_code_raw = response.headers['content-type']
        page.page_type_code = get_content_type(page.page_type_code_raw)
        page.last_accessed_time = int(time.time())
        page.accessed_time = datetime.datetime.now()
        db.update_last_accessed_time(page.site_id, page.last_accessed_time, conn)
        print("craw_page request.head successful", page.page_type_code)

    except Exception as e:
        print("Request head failed :", e)
        
        try:

            time.sleep(page.crawl_delay)
            page.last_accessed_time = int(time.time())
            db.update_last_accessed_time(page.site_id, page.last_accessed_time, conn)
            response = requests.get(page.url_req, allow_redirects=True, timeout=timeout, headers=headers, verify=False)
            page.http_status_code = response.status_code
            page.page_type_code_raw = response.headers['content-type']
            page.page_type_code = get_content_type(page.page_type_code_raw)
            page.last_accessed_time = int(time.time())
            page.accessed_time = datetime.datetime.now()
            db.update_last_accessed_time(page.site_id, page.last_accessed_time, conn)
            print("craw_page request.head successful", page.page_type_code)


        except Exception as e:
            print(e)
            print("crawl_page request failed)")
            page.last_accessed_time = int(time.time())
            page.accessed_time = datetime.datetime.now()
            page.page_type_code_raw = ''
            page.page_type_code = ''
            db.update_last_accessed_time(page.site_id, page.last_accessed_time, page.conn)

        
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

    print(page.page_type_code_raw, page.page_type_code)
    # Content type HTML
    if page.page_type_code == 'HTML':

        time.sleep(page.crawl_delay)
        driver.get(page.url_req)
        time.sleep(timeout) # waiting for page to load

        page.html_content = driver.page_source

        page.accessed_time = datetime.datetime.now()
        page.last_accessed_time = int(time.time())
        #page.hashed_html =  hashlib.md5((page.html_content).encode()).hexdigest()

        # Update page in database
        db.update_page(page.site_id, page.page_type_code, page.url, page.html_content, page.http_status_code, page.accessed_time, page.last_accessed_time, conn)
        print("Page updated in db: ", page.url)

        # get URLs and site_ids from page
        new_urls, site_ids, number = get_urls(driver, conn)

        if number >= 1: 
            write_url_to_frontier(number, new_urls, site_ids, page.url, conn)
        

        # BINARY page_data
        # Types: https://www.iana.org/assignments/media-types/media-types.xhtml
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
    elif page.page_type_code == 'BINARY':

        if 'application/pdf' in page.page_type_code_raw:
            page.page_data_type = 'PDF'
            print(page.page_data_type)
            print(page.page_type_code)
            
            db.write_data(page.page_type_code, page.url, page.http_status_code, page.accessed_time, page.page_data_type, conn)


        elif 'application/msword' in page.page_type_code_raw:
            page.page_data_type = 'DOC'
            print(page.page_data_type)
            print(page.page_type_code)

            db.write_data(page.page_type_code, page.url, page.http_status_code, page.accessed_time, page.page_data_type, conn)


        elif ('application/vnd.openxmlformats-officedocument.wordprocessingml.document' or 'application/octet-stream') in page.page_type_code_raw:
            page.page_data_type = 'DOCX'
            print(page.page_data_type)
            print(page.page_type_code)

            db.write_data(page.page_type_code, page.url, page.http_status_code, page.accessed_time, page.page_data_type, conn)


        elif 'application/vnd.ms-powerpoint' in page.page_type_code_raw:
            page.page_data_type = 'PPT'
            print(page.page_data_type)
            print(page.page_type_code)

            db.write_data(page.page_type_code, page.url, page.http_status_code, page.accessed_time, page.page_data_type, conn)


        elif 'application/vnd.openxmlformats-officedocument.presentationml.presentation' in page.page_type_code_raw:
            page.page_data_type = 'PPTX'
            print(page.page_data_type)
            print(page.page_type_code)

            db.write_data(page.page_type_code, page.url, page.http_status_code, page.accessed_time, page.page_data_type, conn)

            
        elif 'image' in page.page_type_code_raw:
            page.content_type = page.page_type_code_raw
            print(page.page_type_code)
            print(page.content_type)

            db.write_img(page.url, page.site_id, page.page_type_code, page.content_type, page.accessed_time, conn)

        else:
            print("UNKNOW BINARY: ",page.page_type_code_raw)

            db.write_binary(page.page_type_code, page.url, page.http_status_code, page.accessed_time, conn)



def get_urls(driver, conn):
    possible_urls = []

    links_h = driver.find_elements_by_tag_name("a")
    links_b = driver.find_elements_by_xpath("//button[@onclick]")
    #links_s = driver.find_elements_by_xpath("//script")
    links_i=  driver.find_elements_by_tag_name("img")
        

    for link in links_h:
        try:
            l = link.get_attribute('href')
            possible_urls.append(l)
        except:
            pass

    for link in links_b:
        try:
            l = link.get_attribute('onclick')
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
            possible_urls.append(l)
        except:
            pass

    new_urls, site_ids, number = clean_urls(possible_urls, conn)

    return new_urls, site_ids, number



def clean_urls(possible_urls, conn):
    new_urls = []
    site_ids = []
    number = 0

    for url in possible_urls:
        
        if url is None:
            continue
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

        if validated_url != -1:
            if validated_url.endswith(".zip"): # We dont handle zip files
                validated_url = -1

        if validated_url == -1:
            continue

        if '.gov.si' in domain_name(validated_url):

            domain, site_id, disallow = domain_name_new(validated_url, conn)

        #for disa in disallow:
            #if disa not in url:
               # continue

            new_urls.append(validated_url)
            site_ids.append(site_id)
            number = number + 1

    return new_urls, site_ids, number
