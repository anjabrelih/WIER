import os

def get_ip_address(url):
    command = "nslookup " + url
    process = os.popen(command)
    result = str(process.read())
    #print(result)
    marker = result.find('Addresses: ') + 46
    #print(marker)
    #ip_address = result[marker:].splitlines()[0]
    #print(ip_address)
    return result[marker:].splitlines()[0]

print(get_ip_address('www.evem.gov.si'))
#get_ip_address('www.gov.si')

