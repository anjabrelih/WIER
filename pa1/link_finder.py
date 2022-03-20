from html.parser import HTMLParser
from urllib import parse

## Zrihtaj parsanje cele spletne strani tukej! al pa vsaj slike dodej pa parsej vsebino drugot?

class LinkFinder(HTMLParser):
    
    def __init__(self, page_url):
        super().__init__()
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.page_url, value)
                    self.links.add(url)
                

    def page_links(self):
        return self.links


    def error(self, message):
        pass


#finder = LinkFinder()
#finder.feed('<img src="https://ci3.googleusercontent.com/proxy/4hkDsU17S9jMAAzWbFoEMK2dWmfrDjqyYXg5hsBVleM7HZqvIvi1zenvFlgeyUh9gEBqXvskI-r-swqod-qXfW3R0CWjUkZxX4eyv66xLGveTMTr2HrUZYPHzX5h8lAQ5Zp5qUkoWQGWYm9DnU6KmFPMURNEZejnMp0EQVns2oC8GFtq7QgSR-sh7L8VRpwkmwbO4VFazCZdvB34Z16BIZMPx0DrHZNiATau-yJEScN4jyquu96QOwOpU8hV0D514PnVj-nZmwJhQUEqNKHPfGU6J-hUxHAe5sd8txq7ACiHjBDHYArjNUa-fzGQ_8ERLdaPx0gHtJ_XMGYEDHwCzCKwacaLnaRT3HRRIh0110PUjCtwasMndoeIrxqnVLAKLvtr37fWn9AposUf6pKnF3f8dgmJ2ZaaLIJRP-TFEjbZHI97064L6J4CLaciLe0f-9Qv8eBKUon0sWio0jEn5f_ZJaz8RtBYjBvYx2Snch3fWfGZo9Z_lfW1lD0NMAtEua3IUC-GVA7Mp1zqRufRub8t=s0-d-e1-ft#https://postoffice.adobe.com/po-server/link/open?source=eyJhbGciOiJIUzUxMiJ9.eyJ0ZW1wbGF0ZSI6ImNjX2NvbGxhYl94ZF9kb2N1bWVudF9pbnZpdGVfbm90aWZpY2F0aW9uIiwiZW1haWxBZGRyZXNzIjoiYnJlbGloLmFuamFAZ21haWwuY29tIiwicmVxdWVzdElkIjoiMGQ3Y2VjZDMtMTQ4OC00NjI3LTc2ZWMtYzk4ZDlhNGE2ZGMwIiwibG9jYWxlIjoiZW5fVVMifQ.pn2bx-fn2HjH5SZPulZlNJ9xKcvpFH_xBp9XVWodfzN_YojQdiyoBcPs7W24en01po9pX441_2SaR0k8d07V-g" height="1" width="1" class="CToWUd">')






