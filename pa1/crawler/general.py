import hashlib
import socket
from urllib.parse import urlparse
from attr import validate
from url_normalize import url_normalize
import urllib.request
import io
from validator_collection import validators
from zmq import NULL
import db
import time


# Hash HTML content
def html_hash(html):
    hashed_html = hashlib.md5((html).encode()).hexdigest()

    return hashed_html


# Correct url (before canonicalization!) (output)
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


# We dont need this
# Get (sub)domain name (output example: www.gov.si)
def domain_name(url):
    domain = urlparse(url).netloc

    return domain


# Get (sub)domain name (output example: www.gov.si) when getting links from page
def domain_name_new(url):
    url = correct_url(url)
    domain = urlparse(url).netloc

    if domain.startswith("www"):
        pass
    else:
        domain = "www."+domain

    site_id, flag, disallow = db.write_domain_to_site(domain)

    # new domain
    if flag == -1 and site_id != -1:
        try:
            robots_content, sitemap_content, disallow, crawl_delay, last_accessed_time = get_robots_txt(domain)
        except:
            robots_content = ''
            sitemap_content = ''
            disallow = {}
            crawl_delay = 5
            last_accessed_time = int(time.time())

        ip_address = get_ip_address(domain)
        db.update_site(site_id, domain, robots_content, sitemap_content, ip_address, crawl_delay, last_accessed_time, disallow)
        print('bd domain updated')
        url = check_potential_url(domain)
        db.write_url_to_frontier(1, url, site_id, url) # write domain to frontier # 1 for link_tree
        
    return domain, site_id, disallow
    


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

    req = urllib.request.urlopen("http://"+ path + "robots.txt", data=None)
    data = io.TextIOWrapper(req, encoding='utf-8')

    robots = data.read()
    last_accessed_time = int(time.time())    
    sitemap, disallow, delay = get_robots_info(robots)

    return robots, sitemap, disallow, delay, last_accessed_time


# Get robots.txt relavant information
def get_robots_info(robots):

    sitemap = []
    disallow = {}
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


# Get content type
def get_content_type(response):
    content_type = 'BINARY'
    if 'html' in response:
        content_type = 'HTML'
    return content_type
    

# Check potential url
def check_potential_url(url):
    try:
        url = url_canonical(url)
        validated = validators.url(url)
        if validated.startswith("https://"):
            validated = validated[8:]
        if validated.startswith("http://"):
            validated = validated[7:]
        if validated.endswith("/"):
            validated = validated[:-1]
        if validated.startswith("www"):
            pass
        else:
            validated = "www."+validated

    except:
        validated = -1

    return validated

