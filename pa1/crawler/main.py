import threading
import time
import crawler
from db import *
import general



# Set seeds for web crawler
seeds = ['https://www.gov.si/','http://evem.gov.si/', 'https://e-uprava.gov.si/', 'https://www.e-prostor.gov.si/']
# Set number of threads for web crawler
number_of_threads = 5


# Get frontier
frontier_size = get_frontier_size()

if frontier_size == 0:
        for link in seeds:
            domain, site_id, disallow = general.domain_name(link)
            write_url_to_frontier(1, link, site_id) # site ID check! - probs need to check domain here - for later links it's gonna be in linkfinder?
            print('Seed in frontier: ',link)

        frontier_size = get_frontier_size()


# Create worker threads
while frontier_size != -1:
    i = 0
    threads = []

    
    if i >= number_of_threads:
        break

    url = get_url_from_frontier()
    if url == -1:
        time.timeout(5)
        url = get_url_from_frontier()

    t = threading.Thread(target = crawler.crawl_page(url))
    t.daemon = True
    t.start()
    threads.append(t)
    i = i + 1

    for th in threads:
        th.join()
    
    frontier_size = get_frontier_size()


