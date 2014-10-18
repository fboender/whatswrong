import re

__ident__ = 'ssh::root_login'
__severity__ = 4
__impact__ = 4
__cost_to_fix__ = 1
__fail_msg__ = 'SSH allows remote root logins'
__explanation__ = ''

def scan():
    fc = file('/etc/ssh/sshd_config', 'r').read().lower()
    matches = re.findall('.*permitrootlogin.*', fc)
    if matches and matches[0].endswith('yes'):
        return True
    else:
        return False


