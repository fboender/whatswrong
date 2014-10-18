import scanner
import re

__ident__ = 'ssh::empty_passwords'
__severity__ = 5
__impact__ = 2
__cost_to_fix__ = 1
__explanation__ = ''

def scan():
    fc = file('/etc/ssh/sshd_config', 'r').read().lower()
    matches = re.findall('.*permitemptypasswords.*', fc)
    if matches and matches[0].endswith('yes'):
        return (scanner.FAIL, 'The SSH server allows empty passwords')
    else:
        return (scanner.PASS, 'The SSH server does not allow empty passwords')
