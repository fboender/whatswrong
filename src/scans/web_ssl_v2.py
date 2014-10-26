import scanner
import httplib
import ssl
import socket

__ident__ = 'web::ssl::v2'
__severity__ = 5
__impact__ = 3
__cost_to_fix__ = 1
__fail_msg__ = 'The webserver supports SSLv2, which is broken'
__explanation__ = '''SSL v2 is no longer secure and should not be enabled'''

def scan():
    if not hasattr(ssl, 'PROTOCOL_SSLv2'):
        return (scanner.ERROR, "SSLv2 Protocol not supported by Python")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        ssl_sock = ssl.wrap_socket(s, ca_certs="/etc/ca_certs_file", ssl_version=ssl.PROTOCOL_SSLv2)
        ssl_sock.connect(('127.0.0.1', 443))
        ssl_sock.close()
        return (scanner.FAIL, 'The webserver supports SSLv2, which is broken')
    except ssl.SSLError, e:
        return (scanner.NA, "Can't test for SSLv2: %s" % (str(e)))
    return (scanner.PASS, 'The webserver doesn\'t support SSLv3')
