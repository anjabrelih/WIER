import threading
from queue import Queue

from zmq import QUEUE
from spider import Spider
from domain import *
from general import *
import time


PROJECT_NAME = 'Pajek Oskar'
HOMEPAGE1 = 'https://www.gov.si/'
HOMEPAGE2 = 'http://evem.gov.si/evem/drzavljani/zacetna.evem'
HOMEPAGE3 = 'https://e-uprava.gov.si/'
HOMEPAGE4 = 'https://www.e-prostor.gov.si/'


DOMAIN_NAME1 = get_domain_name(HOMEPAGE1)
DOMAIN_NAME2 = get_domain_name(HOMEPAGE2)
DOMAIN_NAME3 = get_domain_name(HOMEPAGE3)
DOMAIN_NAME4 = get_domain_name(HOMEPAGE4)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 5     #ŠTEVILO NITI
TIMEOUT = 5
queue = Queue()   #THREAD QUEUE

Spider(PROJECT_NAME, HOMEPAGE1,HOMEPAGE2,HOMEPAGE3,HOMEPAGE4, DOMAIN_NAME1,DOMAIN_NAME2,DOMAIN_NAME3,DOMAIN_NAME4)




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
        time.sleep(TIMEOUT)
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

















