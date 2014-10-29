import scanner
import re

__ident__ = 'mysql::listen'
__severity__ = 3
__impact__ = 3
__cost_to_fix__ = 1
__explanation__ = '''Service that listen on 0.0.0.0 will accept connections from
any IP. This can cause security problems if the machine is exposed to different
networks or if the firewall fails for some reason. Ideally, services should
only listen on localhost (127.0.0.1) or otherwise on a specific IP'''

def scan():
    found = 0
    for line in file('/etc/mysql/my.cnf', 'r'):
        if line.strip().startswith('#'):
            continue

        if line.startswith('bind-address') and \
           line.strip().endswith('0.0.0.0'):
            return scanner.Result(scanner.FAIL, 'MySQL is listening on all addresses')

    return scanner.Result(scanner.PASS, 'MySQL is not listening on all addresses')
