from urllib.request import urlopen
from webbrowser import get
from link_finder import LinkFinder
from general import * #import all
from domain import *


class Spider:

    #Class variables (shared among all instances/spiders)
    project_name = ''
    queue_file = ''   #text file saved on hard drive
    crawled_file = ''  #text file saved on hard drive
    DOMAIN_file = ''
    queue = set()      #stored on RAM -> faster
    crawled = set()     #stored on RAM -> faster
    domain = set()

    def __init__(self, project_name,base_url1):
        Spider.project_name = project_name
        Spider.base_url1 = base_url1            #SHARED INFORMATION
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
        #Spider.queue.add('https://www.gov.si/') se naredi že na začetku
        Spider.queue.add('http://evem.gov.si/evem/drzavljani/zacetna.evem')
        Spider.queue.add('https://e-uprava.gov.si/')
        Spider.queue.add('https://www.e-prostor.gov.si/')
        

    @staticmethod
    def crawl_page(thread_name, page_url): #page_url from queue.txt
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()


    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url1)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()  


    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled): #Preverimo duplikate linkov
                continue
            if 'gov.si' in url : #Pajek ne shranjuje linkov, ki ne vsebujejo gov.si
                Spider.queue.add(url)

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
