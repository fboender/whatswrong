import scanner
import re

__ident__ = 'mysql::listen'
__severity__ = 3
__impact__ = 3
__cost_to_fix__ = 1
__explanation__ = ''

def scan():
    found = 0
    for line in file('/etc/mysql/my.cnf', 'r'):
        if line.strip().startswith('#'):
            continue

        if line.startswith('bind-address') and \
           line.strip().endswith('0.0.0.0'):
            return (scanner.FAIL, 'MySQL is listening on all addresses')

    return (scanner.PASS, 'MySQL is not listening on all addresses')
