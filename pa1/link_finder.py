from html.parser import HTMLParser
from urllib import parse


class LinkFinder(HTMLParser):
    
    def __init__(self, base_url1,base_url2,base_url3,base_url4, page_url):
        super().__init__()
        self.base_url1 = base_url1
        self.base_url2 = base_url2
        self.base_url3 = base_url3
        self.base_url4 = base_url4
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url1 = parse.urljoin(self.base_url1, value)
                    self.links.add(url1)
                    url2 = parse.urljoin(self.base_url1, value)
                    self.links.add(url2)
                    url3 = parse.urljoin(self.base_url1, value)
                    self.links.add(url3)
                    url4 = parse.urljoin(self.base_url1, value)
                    self.links.add(url4)


    def page_links(self):
        return self.links


    def error(self, message):
        pass


#finder = LinkFinder()
#finder.feed('<html><head><title><Test></title></head>')








