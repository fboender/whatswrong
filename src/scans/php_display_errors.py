import scanner
import tools
import re
import os

__ident__ = 'php::display_errors'
__severity__ = 5
__impact__ = 4
__cost_to_fix__ = 1
__explanation__ = ''

def scan():
    php_inis = [
        '/etc/php5/apache2/php.ini',
        '/etc/php5/cli/php.ini',
    ]

    if not os.path.isdir('/etc/php5'):
        return (scanner.NA, 'PHP not found')

    failed = []
    passed = []
    for php_ini in php_inis:
        file(php_ini, 'r').read() # Test file read access. Throws exception if failed.
        code = "echo(ini_get('display_errors'));"
        res = tools.cmd('php -c %s -r "%s"' % (php_ini, code))
        if res['stderr']:
            raise scanner.ScanError('%s: %s' % (php_ini, res['stderr'].replace('\n', '')))
        elif len(res['stdout']) > 6:
            raise scanner.ScanError('%s: %s' % (php_ini, res['stdout'].replace('\n', '')))
        elif res['stdout'] != '' and res['stdout'] != '0' and res['stdout'] != 'STDOUT':
            failed.append('%s has display_errors on' % (php_ini))
        else:
            passed.append('%s does not have display_errors on' % (php_ini))

    if failed:
        return (scanner.FAIL, ', '.join(failed))
    else:
        return (scanner.PASS, ', '.join(passed))
