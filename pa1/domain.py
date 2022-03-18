from urllib.parse import urlparse


#Get domain name (npr. ulr = www.gov.si)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.') # -> restults je list : name example com
        return results[-2] + '.' + results[-1]
    except:
        return ''   




#Get sub domain name (www.evem.gov.si)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''


#Test delovanja
#print(get_domain_name('https://e-uprava.gov.si/podrocja/osebni-dokumenti-potrdila-selitev/selitev-prijava-odjava-prebivalisca.html'))
#print(get_sub_domain_name('https://e-uprava.gov.si/podrocja/osebni-dokumenti-potrdila-selitev/selitev-prijava-odjava-prebivalisca.html'))