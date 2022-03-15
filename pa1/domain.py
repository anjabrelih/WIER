from urllib.parse import urlparse


#Get domain name (www.gov.si)
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


#print(get_domain_name('https://mobile.email.ana.thenewboston.com/apps/getmefunky'))