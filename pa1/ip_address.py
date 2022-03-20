import socket


# get domain IP address
def get_ip_address(url):

    ip_addr = socket.gethostbyname(url)

    return ip_addr

print(get_ip_address('gov.si'))