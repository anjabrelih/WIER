from url_normalize import url_normalize
from urllib.parse import urlparse


url = 'https://www.gov.si/dostopnost/#wrapper'
url2 = 'https://e-uprava.gov.si/?view_mode=5'
url3 = 'https://www.gov.si/novice/?tag%5B0%5D=554'


parse = urlparse(url3)
#print(parse)

url_can = parse.scheme + "://" + parse.netloc + parse.path
#print(url_can)

url_can_norm = url_normalize(url_can)
#print(url_can_norm)
