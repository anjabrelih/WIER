from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import datetime
from urllib.parse import urldefrag

from db import *
from general import *
from thread import *


class Crawler:

    def __init__(self, timeout, web_driver_location, user_agent, headers, instance):

        self.INSTANCE = instance
        self. TIMEOUT = timeout
        self.WEB_DRIVER_LOCATION = web_driver_location
        self.USER_AGENT = user_agent
        self.HEADERS = headers

        # Options (do not edit)
        self.CHROME_OPTIONS = Options()
        self.CHROME_OPTIONS.add_argument("--headless")
        self.CHROME_OPTIONS.add_argument(user_agent)
        self.CHROME_OPTIONS.add_argument('ignore-certificate-errors') # ignore certificate errors to disable SSL cert. error
        self.DRIVER = webdriver.Chrome(executable_path=self.WEB_DRIVER_LOCATION, options=self.CHROME_OPTIONS)



# Crawl page
    def crawl_page(self, url):


        # Get job info
        crawl_delay, site_id, last_accessed_time, lock = get_job_info(url) #tukej moreš zaklenit domeno (urlje brez problema podeliš)
        page_type_code_raw = ''
        page_type_code = ''

        # lock: 0 - unlocked; 1 - locked
        while lock == 1:
            print('WAITING TO UNLOCK')
            time.sleep(3)
            crawl_delay, site_id, last_accessed_time, lock = get_job_info(url)
            


        # Check last accessed time and crawl delay - if needed sleep
        try:
            time_passed = int(int(time.time()) - last_accessed_time)
        except:
            time_passed = int(1)

        # Check is if crawl_delay is int in case there is a problem in db and crawl_delay isnt logged
        if isinstance(crawl_delay, int):
            pass
        else:
            crawl_delay = 5

        if time_passed < crawl_delay:
            time.sleep(crawl_delay-time_passed)
        
          

        # In case url doesnt start with protocol
        if url.startswith('www'):
            url_req = 'http://'+ url
        else:
            url_req = url
 
        try:
            response = requests.head(url_req, allow_redirects=True, timeout=self.TIMEOUT, headers=self.HEADERS, verify=False) #verify false to disable SSL cert. error
            http_status_code = response.status_code
            page_type_code_raw = response.headers['content-type']
            page_type_code = get_content_type(page_type_code_raw)
            last_accessed_time = int(time.time())
            accessed_time = datetime.datetime.now()
            print("craw_page request.head successful", page_type_code)
            if page_type_code == 'HTML':
                lock = 1
            else:
                lock = 0
            db.update_last_accessed_time(site_id, last_accessed_time, lock)
            print("LOCK/UNLOCK", lock) 

        except Exception as e:
            print("Request head failed :", e)
        
            try:
                # Retry requests.get after crawl delay
                time.sleep(crawl_delay)
                response = requests.get(url_req, allow_redirects=True, timeout=self.TIMEOUT, headers=self.HEADERS, verify=False)
                http_status_code = response.status_code
                page_type_code_raw = response.headers['content-type']
                page_type_code = get_content_type(page_type_code_raw)
                last_accessed_time = int(time.time())
                accessed_time = datetime.datetime.now()
                #db.update_last_accessed_time(site_id, last_accessed_time)
                print("craw_page request.head successful", page_type_code)
                if page_type_code == 'HTML':
                    lock = 1
                else:
                    lock = 0
                db.update_last_accessed_time(site_id, last_accessed_time, lock)
                print("LOCK/UNLOCK", lock) 


            except Exception as e:
                print(e)
                print("crawl_page request failed)")
                last_accessed_time = int(time.time())
                accessed_time = datetime.datetime.now()
                page_type_code_raw = ''
                page_type_code = ''
                lock = 0
                db.update_last_accessed_time(site_id, last_accessed_time, lock)
                print("LOCK/UNLOCK", lock) 
                return



       


        print(page_type_code_raw, page_type_code)
        # Content type HTML
        if page_type_code == 'HTML':

        
            try:
                time.sleep(crawl_delay)
                self.DRIVER.get(url_req)
                time.sleep(self.TIMEOUT) # waiting for page to load

                html_content = self.DRIVER.page_source

                accessed_time = datetime.datetime.now()
                last_accessed_time = int(time.time())
                #page.hashed_html =  hashlib.md5((page.html_content).encode()).hexdigest() # moved to db.update_page

                # Update page in database
                id = db.update_page(site_id, page_type_code, url, html_content, http_status_code, accessed_time, last_accessed_time)
                print(self.INSTANCE, " Page updated in db: ", url)


                # get new URLs and site_ids from page
                new_urls, site_ids, number = self.get_urls(self.DRIVER)

                if number >= 1: 
                    write_url_to_frontier(number, new_urls, site_ids, url)
                
            except:
                # Used in case getting page with selenium failes
                id = db.update_page1(site_id, page_type_code, url, http_status_code, accessed_time, last_accessed_time)
                print(self.INSTANCE, "HTML page updated in db: ", url)
        

        # BINARY page_data
        # Types: https://www.iana.org/assignments/media-types/media-types.xhtml
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
        elif page_type_code == 'BINARY':

            if 'application/pdf' in page_type_code_raw:
                page_data_type = 'PDF'
                print(page_data_type)
                print(page_type_code)
            
                db.write_data(page_type_code, url, http_status_code, accessed_time, page_data_type)


            elif 'application/msword' in page_type_code_raw:
                page_data_type = 'DOC'
                print(page_data_type)
                print(page_type_code)

                db.write_data(page_type_code, url, http_status_code, accessed_time, page_data_type)


            elif ('application/vnd.openxmlformats-officedocument.wordprocessingml.document' or 'application/octet-stream') in page_type_code_raw:
                page_data_type = 'DOCX'
                print(page_data_type)
                print(page_type_code)

                db.write_data(page_type_code, url, http_status_code, accessed_time, page_data_type)


            elif 'application/vnd.ms-powerpoint' in page_type_code_raw:
                page_data_type = 'PPT'
                print(page_data_type)
                print(page_type_code)

                db.write_data(page_type_code, url, http_status_code, accessed_time, page_data_type)


            elif 'application/vnd.openxmlformats-officedocument.presentationml.presentation' in page_type_code_raw:
                page_data_type = 'PPTX'
                print(page_data_type)
                print(page_type_code)

                db.write_data(page_type_code, url, http_status_code, accessed_time, page_data_type)

            
            elif 'image' in page_type_code_raw:
                content_type = page_type_code_raw
                print(page_type_code)
                print(content_type)

                db.write_img(url, site_id, page_type_code, content_type, accessed_time)

            # For binary data types that we dont handle
            else:
                print("UNKNOW BINARY: ",page_type_code_raw)

                db.write_binary(page_type_code, url, http_status_code, accessed_time)

        return



    def get_urls(self, driver):
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

        new_urls, site_ids, number = self.clean_urls(possible_urls)

        return new_urls, site_ids, number



    def clean_urls(self, possible_urls):
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
            
            # Fragment identifier
            url = urldefrag(url)[0]

            if url.endswith("/"):
                url = url[:-1]

            if url.endswith("/index.html"):
                url = url[:-11]

            if url.endswith("/index.php"):
                url = url[:-10]

        
            validated_url = check_potential_url(url) # returns -1 if not URL

            if validated_url != -1:
                if validated_url.endswith(".zip"): # We dont handle zip files
                    validated_url = -1

            if validated_url == -1:
                continue

            # Check if url is from domain name gov.si
            if '.gov.si' in domain_name(validated_url):

                # Get domain info (and insert new domain if it doesnt exist yet)
                domain, site_id, robots_content = domain_name_new(validated_url)

                if robots_content != '':
                    disallow = []
                    lines = str(robots_content).splitlines()

                    for line in lines:
                        # Check disallow
                        if 'disallow:' in line.lower():
                            disallow.append(line.split(': ')[1].split(' ')[0])

                    # Check if new url contains disallow
                    for dis in disallow:
                        if dis in validated_url:
                            continue


                new_urls.append(validated_url)
                site_ids.append(site_id)
                number = number + 1

        return new_urls, site_ids, number


    def close_crawler(self):
        self.DRIVER.close()