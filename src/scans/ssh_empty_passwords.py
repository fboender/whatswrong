import re

__ident__ = 'ssh::empty_passwords'
__severity__ = 5
__impact__ = 2
__cost_to_fix__ = 1
__fail_msg__ = 'SSH allows empty passwords'
__explanation__ = ''

def scan():
    fc = file('/etc/ssh/sshd_config', 'r').read().lower()
    matches = re.findall('.*permitemptypasswords.*', fc)
    if matches and matches[0].endswith('yes'):
        return True
    else:
        return False

