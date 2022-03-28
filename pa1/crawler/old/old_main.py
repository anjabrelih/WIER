import threading
import time
import old_crawler
from old_db import *
import old_general
from queue import Queue
lock = threading.Lock()
from old_page import Page, Page1, Page2, Page3



# Set seeds for web crawler
seeds = ['https://www.gov.si','http://evem.gov.si', 'https://e-uprava.gov.si', 'https://www.e-prostor.gov.si']

# Set number of threads for web crawler
number_of_threads = 1
#queue = Queue()

# When initializing
# One master connection for controling frontier size
connMaster = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")

frontier_size = get_frontier_size(connMaster)
print(frontier_size)


# Start procedure
if frontier_size == 0:
    for link in seeds:
        domain, site_id, disallow = general.domain_name_new(link, connMaster)
        print('Seed in frontier: ',link)


# Create thread number of connections
connect = []
for i in range(number_of_threads):
    connect.append(psycopg2.connect(host="localhost", user="crawler", password="SecretPassword"))
    #for conn in connect:
       # conn.autocommit = True




# Working thread
def work(conn, thread):
    while True:
        #lock.acquire()
        url, crawl_delay, site_id, last_accessed_time = get_url_from_frontier(conn)
        if thread == 0:
            page = Page
        elif thread == 1:
            page = Page1
        elif thread == 2:
            page = Page2
        elif thread == 3:
            page = Page3

        page.url = url
        page.crawl_delay = crawl_delay
        page.site_id = site_id

        try:
            time_passed = int(int(time.time()) - last_accessed_time)
        except:
            time_passed = int(1)

        if isinstance(crawl_delay, int):
            pass
        else:
            crawl_delay = 5

        if time_passed >= crawl_delay:
            crawler.crawl_page(threading.current_thread().name, page, conn)#, crawl_delay, site_id, conn)

        else:
            time.sleep(crawl_delay-time_passed)
            crawler.crawl_page(threading.current_thread().name, page, conn) #, crawl_delay, site_id, conn)

        #lock.release()

# Create threads
while frontier_size > 0:
    i = 0
    threads = []
    for i in range(number_of_threads): 
        t = threading.Thread(target = work, args=(connect[i],i))
        print("thread ", i, " started working")
        t.start()
        threads.append(t)
        i = i + 1

    for th in threads:
        th.join()

    frontier_size = get_frontier_size(connMaster)

# Close connections    
connMaster.close()
for i in range(number_of_threads):
    connect[i].close()



# Each FRONTIER link is a new job
#def create_jobs(test):
 #   while test > 0:
   #     url = get_url_from_frontier()
   #     queue.put(url)
  #     test = test - 1
   # time.sleep(75)    
   # crawl()



# Check if there are items in queue, if so then crawl
#def crawl():
  #  test = 1
  #  frontier_size = get_frontier_size()
  #  print("GETTING frontier size: ",frontier_size)
  #  if (frontier_size != 0) and (frontier_size >= 20):
  #      test = 20
  #  elif (frontier_size != 0) and (frontier_size < 20):
  #      test = frontier_size
  #  else:
  #      test = 0
  #  print(test)

  #  while test > 0:    
  #      create_jobs(test)
  #      print("TO DO: ", frontier_size)
  #      test = test - 1


#start_procedure()
##crawl()

#0ueue.join()



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

