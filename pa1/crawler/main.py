import threading
import datetime
import crawler
import db


# Set seeds for web crawler
seeds = ['https://www.gov.si/','http://evem.gov.si/', 'https://e-uprava.gov.si/', 'https://www.e-prostor.gov.si/']
# Set number of threads for web crawler
number_of_threads = 5

# Get frontier
frontier = db.get_url_from_frontier(number_of_threads) # -1 if empty

if frontier == -1 and len(frontier) == 0:
    for link in seeds:
        db.write_url_to_frontier(link, '') # site ID check! - probs need to check domain here - for later links it's gonna be in linkfinder?
    frontier = db.get_url_from_frontier(number_of_threads)


# Create worker threads
while frontier != -1 and len(frontier) != 0:

#def create_workers():
    for _ in (number_of_threads):
        t = threading.Thread(target = work) # nope, find better way ... target is crawler.crawl_page
        t.daemon = True
        t.start()



