import threading
from db import *
from crawlerOskar import Crawler


### Edit paramsters
TIMEOUT = 5
WEB_DRIVER_LOCATION = "C:/Users/anjab/Downloads/chromedriver_win32/chromedriver"
USER_AGENT = "user-agent=fri-ieps-OSKAR"
HEADERS = {'User-Agent': 'fri-ieps-OSKAR'}


lock = threading.Lock()

# Create threading class (https://levelup.gitconnected.com/multi-threaded-python-web-crawler-for-https-pages-e103f0839b71)
class CrawlerThread(threading.Thread):
    def __init__(self, thread):
        threading.Thread.__init__(self)
        self.thread = thread
        self.crawler = Crawler(TIMEOUT, WEB_DRIVER_LOCATION, USER_AGENT, HEADERS, thread)


    def run(self):
        while True:
            with lock:
                url = db.get_url_from_frontier1()
                print("Thread ", self.thread," got URL ", url)

            if url != "":
                try:
                    self.crawler.crawl_page(url)
                except Exception as e:
                    print("Error didnt start crawling", e)

            else:
                self.close_thread()
                return


# Closing crawler
def close_thread(self):
    self.crawler.close_crawler()











    