import threading
import crawler
import db
from queue import Queue


# Set seeds for web crawler
seeds = ['https://www.gov.si/','http://evem.gov.si/', 'https://e-uprava.gov.si/', 'https://www.e-prostor.gov.si/']
# Set number of threads for web crawler
number_of_threads = 5


# Get frontier
frontier_url = db.get_url_from_frontier(number_of_threads) # -1 if empty

if frontier_url == -1 and len(frontier_url) == 0:
    try:
        for link in seeds:
            db.write_url_to_frontier(link, '') # site ID check! - probs need to check domain here - for later links it's gonna be in linkfinder?
        frontier_url = db.get_url_from_frontier(number_of_threads) # do I need this here?
        print('seed in db')
    except:
        print("No more urls")


# Create worker threads
while frontier_url != -1 and len(frontier_url) != 0:
    i = 0
    threads = []

    for f_url in frontier_url:

        if i >= number_of_threads:
            break

        t = threading.Thread(target = crawler.crawl_page(f_url))
        t.daemon = True
        t.start()
        threads.append(t)
        i = i + 1

    for th in threads:
        th.join()
    
    frontier_url = db.get_url_from_frontier(number_of_threads)


