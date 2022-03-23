import hashlib
import socket
from urllib.parse import urlparse
from url_normalize import url_normalize
import urllib.request
import io
from validator_collection import validators
import requests


# Hash HTML content
def html_hash(html):
    hashed_html = hashlib.md5((html).encode()).hexdigest()

    return hashed_html


# Correct url (before canonicalization!)
def correct_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
        
    return url


# URL canonicalization
def url_canonical(url):
    parse_url = urlparse(correct_url(url))
    url_can = parse_url.scheme + "://" + parse_url.netloc + parse_url.path
    url_can_norm = url_normalize(url_can)

    return url_can_norm


# Get (sub)domain name
def domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''


# Get domain IP address
def get_ip_address(url):
    try:
        return socket.gethostbyname(url)
    except:
        return ''



# Get robots.txt content
def get_robots_txt(domain_url):
    if domain_url.endswith('/'):
        path = domain_url
    else:
        path = domain_url + '/'

    req = urllib.request.urlopen(path + "robots.txt", data=None)
    data = io.TextIOWrapper(req, encoding='utf-8')

    robots = data.read()    
    sitemap, disallow, delay = get_robots_info(robots)

    return robots, sitemap, disallow, delay


# Get robots.txt relavant information
def get_robots_info(robots):

    sitemap = []
    disallow = []
    delay = 5 # Default value
    lines = str(robots).splitlines()

    for line in lines:
        # Sitemap
        if 'sitemap:' in line.lower(): # line.lower ot avoid upper/lower case problem
            split = line.split(': ')
            print(split)
                        
            for possible_link in split: 
                try:
                    value = validators.url(possible_link)
                    sitemap.append(value)
                    print(sitemap)
                except:
                    pass
        
        # Disallow
        if 'disallow:' in line.lower():
            disallow.append(line.split(': ')[1].split(' ')[0])

        # Crawl-delay
        if ('crawl-delay:' or 'crawl delay:' or 'crawl_delay:') in line.lower():
            split = line.split(': ')[1]
            delay = int(split)
     
    return sitemap, disallow, delay