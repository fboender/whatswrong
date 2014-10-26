import scanner
import re

__ident__ = 'ssh::root_login'
__severity__ = 4
__impact__ = 4
__cost_to_fix__ = 1
__explanation__ = '''The root account has all the priviliges on a system. It
should not be directly exposed to the outside world.'''

def scan():
    fc = file('/etc/ssh/sshd_config', 'r').read().lower()
    matches = re.findall('.*permitrootlogin.*', fc)
    if matches and matches[0].strip().endswith('yes'):
        return (scanner.FAIL, 'SSH allows remote root logins')
    else:
        return (scanner.PASS, 'SSH does not allow remote root logins')


