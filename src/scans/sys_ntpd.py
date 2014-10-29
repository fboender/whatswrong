import scanner
import tools

__ident__ = 'sys::ntpd'
__severity__ = 4
__impact__ = 2
__cost_to_fix__ = 1
__explanation__ = '''NTPd is a daemon that keeps the system time ''' \
                  '''synchronised. Unsychronised server times can lead to ''' \
                  '''strange unexplained major problems '''

def scan():
    res = tools.cmd('pidof ntpd')
    if res['exitcode'] != 0:
        return scanner.Result(scanner.FAIL, 'NTPd is not running')
    else:
        return scanner.Result(scanner.PASS, 'NTPd is running')
