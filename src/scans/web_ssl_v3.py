import httplib
import ssl
import socket

__ident__ = 'web::ssl::v3'
__severity__ = 5
__impact__ = 3
__cost_to_fix__ = 1
__fail_msg__ = 'The webserver supports SSLv3, which is broken'
__explanation__ = ''

def scan():
    if not hasattr(ssl, 'PROTOCOL_SSLv3'):
        raise ScanError("SSLv3 Protocol not supported by Python")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        ssl_sock = ssl.wrap_socket(s, ca_certs="/etc/ca_certs_file", ssl_version=ssl.PROTOCOL_SSLv3)
        ssl_sock.connect(('127.0.0.1', 443))
        print ssl_sock
        ssl_sock.close()
    except ssl.SSLError, e:
        return None
    return True
