import httplib

__ident__ = 'web::ssl::v2'
__severity__ = 5
__impact__ = 3
__cost_to_fix__ = 1
__fail_msg__ = 'The webserver supports SSLv2, which is broken'
__explanation__ = ''

def scan():
    if not hasattr(ssl, 'PROTOCOL_SSLv2'):
        raise ScanError("SSLv2 Protocol not supported by Python")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = ssl.wrap_socket(s, ca_certs="/etc/ca_certs_file", ssl_version=ssl.PROTOCOL_SSLv2)
        ssl_sock.connect(('127.0.0.1', 443))
        ssl_sock.close()
    except ssl.SSLError:
        return None
    return True
