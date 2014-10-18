import httplib

__ident__ = 'web::powered_by'
__severity__ = 3
__impact__ = 1
__cost_to_fix__ = 1
__fail_msg__ = 'The webserver exposes backend software via X-Powered-By headder'
__explanation__ = ''

def scan():
    connection = httplib.HTTPConnection("127.0.0.1")
    connection.request("HEAD", "/")
    response = connection.getresponse()
    fail = False
    for header_name, header_value in response.getheaders():
        if 'powered-by' in header_name.lower():
            return True
    return False
