import urllib.request
import io
from webbrowser import get
from link_finder import LinkFinder

def get_robots_txt(url):
    if url.endswith('/'):
        path = url
    else:
        path = url + '/'

    print(path)
    req = urllib.request.urlopen(path + "robots.txt", data=None)
    data = io.TextIOWrapper(req, encoding='utf-8')

    #sitemap = LinkFinder(data)
    #print('Sitemap found: ', sitemap)

    return data.read()

print(get_robots_txt('https://www.e-prostor.gov.si/'))