import threading
import time
import crawler
from db import *
import general
from queue import Queue



# Set seeds for web crawler
seeds = ['https://www.gov.si','http://evem.gov.si', 'https://e-uprava.gov.si', 'https://www.e-prostor.gov.si']

# Set number of threads for web crawler
number_of_threads = 3
queue = Queue()

# When initializing
# Get frontier
def start_procedure():
    frontier_size = get_frontier_size()

    if frontier_size == 0:

        for link in seeds:
            domain, site_id, disallow = general.domain_name_new(link)
            #url = general.check_potential_url(link)
            print('Seed in frontier: ',link)



#
# Create worker threads
def create_threads():
    for _ in range(number_of_threads):
        t = threading.Thread(target = work)
        t.daemon = True
        t.start()

# Do the job in the queue
def work():
    while True:
        url = queue.get()
 
        crawl_delay, siteid, last_accessed_time = get_job_info(url)

        try:
            time_passed = int(int(time.time()) - last_accessed_time)
        except:
            time_passed = int(1)

        if isinstance(crawl_delay, int):
            pass
        else:
            crawl_delay = 5

        if time_passed >= crawl_delay:
            crawler.crawl_page(threading.current_thread().name, url, crawl_delay, siteid)
            queue.task_done()
        else:
            time.sleep(crawl_delay-time_passed)
            crawler.crawl_page(threading.current_thread().name, url, crawl_delay, siteid)
            queue.task_done()
    


# Each FRONTIER link is a new job
def create_jobs(test):
    while test > 0:
        url = get_url_from_frontier()
        queue.put(url)
        test = test - 1
    time.sleep(75)    
    crawl()



# Check if there are items in queue, if so then crawl
def crawl():
    test = 1
    frontier_size = get_frontier_size()
    print("GETTING frontier size: ",frontier_size)
    if frontier_size > 0 and frontier_size >= 50:
        test = 50
    elif frontier_size > 0 and frontier_size < 50:
        test = frontier_size
    else:
        test = 0

    while test > 0:    
        create_jobs(test)
        print("TO DO: ", frontier_size)
        test = test - 1


start_procedure()
create_threads()
crawl()

queue.join()



# STORE
        

# Create worker threads
#while frontier_size != -1:
   # i = 0
    #threads = []
    
   # if i >= number_of_threads:
    #    break

   # url, site_id, crawl_delay, last_accessed_time = get_url_from_frontier()
    
  #  if isinstance(crawl_delay, int):
   #     pass
    #else:
     #   crawl_delay = 5

    #if url == -1:
   #     time.sleep(2)
   #     url = get_url_from_frontier()

 #   try:
  #      time_passed = int(time.time()) - last_accessed_time
  #  except:
   #     time_passed = 1

   # if time_passed >= crawl_delay:

    #    t = threading.Thread(target = crawler.crawl_page(url, crawl_delay, site_id))
    #    t.daemon = True
    #    t.start()
    #    threads.append(t)
    #    i = i + 1

    #else:
   #     time.sleep(crawl_delay-time_passed)
   #     t = threading.Thread(target = crawler.crawl_page(url, crawl_delay, site_id))
   #     t.daemon = True
   #     t.start()
    #    threads.append(t)
    #    i = i + 1

   # for th in threads:
    #    print(th)
    #    th.join()
    
    #frontier_size = get_frontier_size()

