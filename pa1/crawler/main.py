from db import *
import general
from thread import CrawlerThread



# Set seeds for web crawler
seeds = ['https://www.gov.si','http://evem.gov.si', 'https://e-uprava.gov.si/', 'https://www.e-prostor.gov.si']

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


