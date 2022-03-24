import threading
import time
import crawler
from db import *
import general



# Set seeds for web crawler
seeds = ['https://www.gov.si','http://evem.gov.si', 'https://e-uprava.gov.si', 'https://www.e-prostor.gov.si']
# Set number of threads for web crawler
number_of_threads = 4


# Get frontier
frontier_size = get_frontier_size()

if frontier_size == 0:
        for link in seeds:
            domain, site_id, disallow = general.domain_name_new(link)
            url = general.check_potential_url(link)
            write_url_to_frontier(1, url, site_id) # site ID check! - probs need to check domain here - for later links it's gonna be in linkfinder?
            print('Seed in frontier: ',link)

        frontier_size = get_frontier_size()


# Create worker threads
while frontier_size != -1:
    i = 0
    threads = []
    
    if i >= number_of_threads:
        break

    url, site_id, crawl_delay, last_accessed_time = get_url_from_frontier()
    
    if isinstance(crawl_delay, int):
        pass
    else:
        crawl_delay = 5

    if url == -1:
        time.sleep(5)
        url = get_url_from_frontier()

    try:
        time_passed = int(time.time()) - last_accessed_time
    except:
        time_passed = 1

    if time_passed >= crawl_delay:

        t = threading.Thread(target = crawler.crawl_page(url, crawl_delay, site_id))
        t.daemon = True
        t.start()
        threads.append(t)
        i = i + 1

    else:
        time.sleep(crawl_delay-time_passed)
        t = threading.Thread(target = crawler.crawl_page(url, crawl_delay, site_id))
        t.daemon = True
        t.start()
        threads.append(t)
        i = i + 1

    for th in threads:
        print(th)
        th.join()
    
    frontier_size = get_frontier_size()


