import scanner
import httplib
import re

__ident__ = 'web::server_banner'
__severity__ = 3
__impact__ = 1
__cost_to_fix__ = 1
__explanation__ = '''Automated malicious vulnerability scanners can pinpoint
exploiits in software more easily if they know the specific version of the
software that's running.'''

def scan():
    connection = httplib.HTTPConnection("127.0.0.1")
    connection.request("GET", "/index.html")
    response = connection.getresponse()
    match = re.match('.*[0-9]+\..*', response.getheader('server', '').lower())
    if match:
        return scanner.Result(scanner.FAIL, 'The webserver exposes a header with version number')
    return scanner.Result(scanner.PASS, 'The webserver doesn\'t exposes a header with version number')
