import scanner
import tools

__ident__ = 'mysql::no_root_pw'
__severity__ = 3
__impact__ = 3
__cost_to_fix__ = 1
__explanation__ = '''The MySQL server's root account does not have a password
set. This is commonly a initial setup mistake.'''

def scan():
    res = tools.cmd('mysql -u root -h 127.0.0.1 -e "exit" ')
    if 'access denied' in res['stderr'].lower():
        return scanner.Result(scanner.PASS, 'The MySQL root account has a password')
    return scanner.Result(scanner.FAIL, 'The MySQL root account has no password')
