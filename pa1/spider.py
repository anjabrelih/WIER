from urllib.request import urlopen
from webbrowser import get
from link_finder import LinkFinder
from general import *
from domain import *
import time
import concurrent.futures
import threading
import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



WEB_DRIVER_LOCATION = "/Users/anjab/Downloads/chromedriver_win32/chromedriver"
TIMEOUT = 5


class Spider:

    #Class variables (shared among all instances/spiders)
    project_name = ''
    queue_file = ''   #text file saved on hard drive
    crawled_file = ''  #text file saved on hard drive
    DOMAIN_file = ''
    queue = set()      #stored on RAM -> faster
    crawled = set()     #stored on RAM -> faster
    domain = set()
    lock = threading.Lock() # threading lock for db

    def __init__(self, project_name, base_url1, base_url2, base_url3, base_url4):
        Spider.project_name = project_name
        Spider.base_url1 = base_url1            #SHARED INFORMATION
        Spider.base_url2 = base_url2
        Spider.base_url3 = base_url3
        Spider.base_url4 = base_url4
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.DOMAIN_file = Spider.project_name + '/DOMAIN.txt'
        self.boot()
        self.crawl_page('First Spider', Spider.base_url1) #prvi pajek odpre začetne strani


 #Z začetka uporabimo samo enega pajka ker imamo v queue.txt samo en (štiri) link
 #Ko naberemo več linkov lahko zaženemo še ostale pajke       

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url1)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)
        Spider.domain = file_to_set(Spider.DOMAIN_file)
        Spider.queue.add(Spider.base_url1)
        Spider.queue.add(Spider.base_url2)
        Spider.queue.add(Spider.base_url3)
        Spider.queue.add(Spider.base_url4)
        Spider.update_files()
        time.sleep(10)

    @staticmethod
    def crawl_page(thread_name, page_url): #page_url from queue.txt
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            time.sleep(3)
            Spider.update_files()

    # spremeni datatype
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url) #, pri urllib.request.Request (sam itak ne dela javascript)......headers={'User-Agent': 'fri-ieps-Oskar'}
            if 'text/html' in response.getheader('Content-Type'): #pa če je javascript???????
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")

           # chrome_options = Options()
            # If you comment the following line, a browser will show ...
          #  chrome_options.add_argument("--headless")

            #Adding a specific user agent
          #  chrome_options.add_argument("user-agent=fri-ieps-TEST")

           # print(f"Retrieving web page URL '{page_url}'")
           # driver = webdriver.Chrome(WEB_DRIVER_LOCATION, options=chrome_options)
           # driver.get(page_url)

            # Timeout needed for Web page to render (read more about it)
          #  time.sleep(TIMEOUT)

           # html = driver.page_source
            

            finder = LinkFinder(Spider.base_url1)
            finder.feed(html_string)

           # driver.close()

        except Exception as error:
            print(str(error))
            return set()
        return finder.page_links()  


    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled): #Preverimo duplikate linkov
                continue
            if 'gov.si' in url : #Pajek ne shranjuje linkov, ki ne vsebujejo gov.si
                Spider.queue.add(url)
                # v bazo
                #Spider.save_to_db(url)

    @staticmethod
    def add_domain(url):
        sub_domain = get_sub_domain_name(url)
        if sub_domain not in Spider.domain:
            Spider.domain.add(sub_domain)


    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
        set_to_file(Spider.domain, Spider.DOMAIN_file)


    def save_to_db(url):
        with Spider.lock:
            try:
                conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword") # connect to db
                conn.autocommit = True

                cur =conn.cursor()
                
                sql = """INSERT INTO crawldb.page (url) VALUES(%s) RETURNING id;"""
                cur.execute(sql, (url,)) #write to db
                id = cur.fetchone()[0] # get id

                print('Logged into db: '+ url)
                print('ID: ', id)
            
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

            finally:
                if conn is not None:
                    conn.close()

            
            

