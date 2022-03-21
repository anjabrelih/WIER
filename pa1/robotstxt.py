import urllib.request
import io
from webbrowser import get
from link_finder import LinkFinder
import robotexclusionrulesparser
import urllib.robotparser
from spider import Spider

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

robotex = robotexclusionrulesparser.RobotExclusionRulesParser()

#print('robots-txt:')
#print(robotex.parse(get_robots_txt('https://www.fri.uni-lj.si/')))
#print(robotex)
#print(robotex.get_crawl_delay)



# ta ni ok
#print('robot parser:')
#rp = urllib.robotparser.RobotFileParser()
#rp.set_url('https://www.fri.uni-lj.si/')
#rp.read()
#try:
#    delay = rp.crawl_delay('*')
#    print("Crawl delay: ",delay)
#except:
#    print("no crawl delay")

def get_sitemaps(robots):
    """Parse a robots.txt file and return a Python list containing any sitemap URLs found.

    Args:
        robots (string): Contents of robots.txt file.
    
    Returns:
        data (list): List containing each sitemap found.
    """

    data = []
    lines = str(robots).splitlines()

    for line in lines:
        if 'Sitemap:' in line: # tukej je ogromno težav s tem, ker je sitemap kdaj kr lepljen na allow/disallow
            split = line.split(': ')
            data.append(split)
            # mogoče če se da kr linkfinder na robotstxt?
            

    return data
sitemaps = get_sitemaps(get_robots_txt('https://www.e-prostor.gov.si/'))
print(sitemaps)

print('Link finder: ')
finder = LinkFinder('gov.si')
finder.feed(get_robots_txt('https://www.gov.si/'))
# vrne ven podan url? BWO
