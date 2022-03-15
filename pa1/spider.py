from urllib.request import urlopen
from link_finder import LinkFinder
from general import * #import all
from domain import *


class Spider:

    #Class variables (shared among all instances/spiders)
    project_name = ''
    base_url1 = ''
    base_url2 = ''
    base_url3 = ''
    base_url4 = ''
    domain_name1 = ''
    domain_name2 = ''
    domain_name3 = ''
    domain_name4 = ''
    queue_file = ''   #text file saved on hard drive
    crawled_file = ''  #text file saved on hard drive
    queue = set()      #stored on RAM -> faster
    crawled = set()     #stored on RAM -> faster

    def __init__(self, project_name, base_url1,base_url2,base_url3,base_url4, domain_name1,domain_name2,domain_name3,domain_name4):
        Spider.project_name = project_name
        Spider.base_url1 = base_url1            #SHARED INFORMATION
        Spider.base_url2 = base_url2
        Spider.base_url3 = base_url3
        Spider.base_url4 = base_url4
        Spider.domain_name1 = domain_name1
        Spider.domain_name2 = domain_name2
        Spider.domain_name3 = domain_name3
        Spider.domain_name4 = domain_name4
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First Spider', Spider.base_url1) #prvi pajek odpre začetne strani
        self.crawl_page('First Spider', Spider.base_url2)
        self.crawl_page('First Spider', Spider.base_url3)
        self.crawl_page('First Spider', Spider.base_url4)

 #Z začetka uporabimo samo enega pajka ker imamo v queue.txt samo en (štiri) link
 #Ko naberemo več linkov lahko zaženemo še ostale pajke       

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url1,Spider.base_url2,Spider.base_url3,Spider.base_url4)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)
        

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
            finder = LinkFinder(Spider.base_url1,Spider.base_url2,Spider.base_url3,Spider.base_url4, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()  


    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name1 != get_domain_name(url):
                continue
            if Spider.domain_name2 != get_domain_name(url):
                continue
            if Spider.domain_name3 != get_domain_name(url):
                continue
            if Spider.domain_name4 != get_domain_name(url):
                continue
            Spider.queue.add(url)


    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
