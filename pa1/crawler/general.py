import hashlib
import urllib.request

# Hash HTML content
def html_hash(html):
    hashed_html = hashlib.md5((html).encode()).hexdigest()
    return hashed_html


# Get Sitemap link from robots.txt
def get_sitemap(robots):
    for line in robots.splitlines():
        if "sitemap" in line:
            smap = urllib.request.get(line.split(' ')[1]) # Not ok - check robotstxt
            return smap.text


