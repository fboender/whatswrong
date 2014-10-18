import tools

__ident__ = 'mysql::no_root_pw'
__severity__ = 3
__impact__ = 3
__cost_to_fix__ = 1
__fail_msg__ = 'The MySQL root account has no password'
__explanation__ = ''

def scan():
    return False
    res = tools.cmd('mysql -u root -h 127.0.0.1')
    if 'access denied' in res['stderr'].lower():
        return False
    return True
