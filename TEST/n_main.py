<<<<<<< HEAD:TEST/n_main.py
import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
import time


PROJECT_NAME = 'Pajek Oskar'


#DOMAIN_NAME1 = get_domain_name(HOMEPAGE1)
SEED1 = ('https://www.gov.si/')
SEED2 = ('http://evem.gov.si/evem/drzavljani/zacetna.evem')
SEED3 = ('https://e-uprava.gov.si/')
SEED4 = ('https://www.e-prostor.gov.si/')
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
DOMAIN_FILE = PROJECT_NAME + '/DOMAIN.txt'
NUMBER_OF_THREADS = 1     #ŠTEVILO NITI
TIMEOUT = 5
queue = Queue()   #THREAD QUEUE

Spider(PROJECT_NAME, SEED1,SEED2,SEED3,SEED4)



#Create worker threads (will die when main exits)
def create_workers():
    for _ in range (NUMBER_OF_THREADS):
        t = threading.Thread(target = work)
        t.daemon = True
        t.start()



#Do the job in the queue
def work():
    while True:
        url = queue.get()
        #domain = get_domain_name(url)
        Spider.add_domain(url)
        #ROBOTS?? TIMEOUT = ?
        #ČAKANJE = 
        #if sub_domain not in ČAKANJE
        #   print('ZAŽENI')
        #   append_to_file(DOMAIN_FILE,sub_domain)
        #   
        #if sub_domain in ČAKANJE:
        #    print('POČAKAJ')       
        #    time.sleep(TIMEOUT)
        #POBERI CONTENT!!
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()



#Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()  



#Check if there are items in queue, if so then crawl
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links))+ ' links in the queue')
        create_jobs()




create_workers()
crawl()

















=======
import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
import time


PROJECT_NAME = 'Pajek Oskar'


#DOMAIN_NAME1 = get_domain_name(HOMEPAGE1)
SEED1 = ('https://www.gov.si/')
SEED2 = ('http://evem.gov.si/evem/drzavljani/zacetna.evem')
SEED3 = ('https://e-uprava.gov.si/')
SEED4 = ('https://www.e-prostor.gov.si/')
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
DOMAIN_FILE = PROJECT_NAME + '/DOMAIN.txt'
NUMBER_OF_THREADS = 5     #ŠTEVILO NITI
TIMEOUT = 5
queue = Queue()   #THREAD QUEUE

Spider(PROJECT_NAME, SEED1,SEED2,SEED3,SEED4)



#Create worker threads (will die when main exits)
def create_workers():
    for _ in range (NUMBER_OF_THREADS):
        t = threading.Thread(target = work)
        t.daemon = True
        t.start()



#Do the job in the queue
def work():
    while True:
        url = queue.get()
        #domain = get_domain_name(url)
        Spider.add_domain(url)
        #ROBOTS?? TIMEOUT = ?
        #ČAKANJE = 
        #if sub_domain not in ČAKANJE
        #   print('ZAŽENI')
        #   append_to_file(DOMAIN_FILE,sub_domain)
        #   
        #if sub_domain in ČAKANJE:
        #    print('POČAKAJ')       
        #    time.sleep(TIMEOUT)
        #POBERI CONTENT!!
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()



#Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()  



#Check if there are items in queue, if so then crawl
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links))+ ' links in the queue')
        create_jobs()




create_workers()
crawl()

















>>>>>>> 2222ee25120a66730cd14662a9e215446a948541:TEST/main.py
