from url_normalize import url_normalize
from urllib.parse import urlparse


# URL canonicalization
def url_canonical(url):
    parse_url = urlparse(url)
    url_can = parse_url.scheme + "://" + parse_url.netloc + parse_url.path
    url_can_norm = url_normalize(url_can)

    return url_can_norm

