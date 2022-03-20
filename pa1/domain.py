from urllib.parse import urlparse


# Get domain name (www.gov.si)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.') # -> restults je list : name example com
        return results[-2] + '.' + results[-1]
    except:
        return ''   
# Poveži z bazo - poglej, če je rezultat že notr, če ni dodaj crawldb.site + robotstxt & sitemap (site map parsej z link finderjem)


# Get sub domain name (www.evem.gov.si)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''


# Test
#print(get_domain_name('https://e-uprava.gov.si/podrocja/osebni-dokumenti-potrdila-selitev/selitev-prijava-odjava-prebivalisca.html'))
#print(get_sub_domain_name('https://e-uprava.gov.si/podrocja/osebni-dokumenti-potrdila-selitev/selitev-prijava-odjava-prebivalisca.html'))