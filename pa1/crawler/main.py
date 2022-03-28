from db import *
import general
from thread import CrawlerThread



# Set seeds for web crawler
seeds = ['https://www.gov.si','http://evem.gov.si', 'https://e-uprava.gov.si', 'https://www.e-prostor.gov.si']

# Set number of threads for web crawler
number_of_threads = 4


# First check frontier_size
frontier_size = get_frontier_size()
print(frontier_size)

# Start procedure
if frontier_size == 0:
    for link in seeds:
        domain, site_id, robots_content = general.domain_name_new(link)
        print('Seed in frontier: ',link)


# Make threads (Class CrawlerThread)
cr_threads = []
for i in range(number_of_threads):
    current_thread = CrawlerThread(i)
    cr_threads.append(current_thread)

# Start threads
for cr in cr_threads:
    cr.start()






### ARCHIVE ###

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

