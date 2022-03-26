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
frontier_size = get_frontier_size()

if frontier_size == 0:

    for link in seeds:
        domain, site_id, disallow = general.domain_name_new(link)
        url = general.check_potential_url(link)
        #write_url_to_frontier(1, url, site_id, url) # linking self in link_tree bc it's new domain
        print('Seed in frontier: ',link)

        #frontier_size = get_frontier_size()



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
       # crawl_delay = 5


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
def create_jobs():
    crawl_delay = 5
    url, site_id, crawl_delay, last_accessed_time = get_url_from_frontier()

    #try:
    #    time_passed = int(int(time.time()) - last_accessed_time)
    #except:
    #    time_passed = int(1)

    #if isinstance(crawl_delay, int):
    #    pass
    #else:
    #    crawl_delay = 5

    #if time_passed >= crawl_delay:
     #   queue.put(url)
        #queue.join()
    #    crawl(1)
   # else:
      #  new_url, new_site_id, crawl_delay, last_accessed_time = get_new_url(site_id, url)
    queue.put(url)
        #queue.join()
    crawl()



# Check if there are items in queue, if so then crawl
def crawl():
    #global frontier_size
   # if flag == 0:
    frontier_size = get_frontier_size()
    print(frontier_size)
    if frontier_size > 0:
        create_jobs()
        frontier_size = frontier_size -1
        print("TO DO: ", frontier_size)
    #else:
       # if flag == 0:
        #    start_procedure()
       # else:
            #frontier_size = get_frontier_size()

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

