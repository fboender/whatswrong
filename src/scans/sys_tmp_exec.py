import scanner
import tools
import os

__ident__ = 'sys::tmp::executable'
__severity__ = 3
__impact__ = 3
__cost_to_fix__ = 4
__explanation__ = ''

def scan():
    tmp_dirs = [
        '/tmp',
        '/var/tmp',
    ]

    results = []
    for tmp_dir in tmp_dirs:
        try:
            path = os.path.join(tmp_dir, 'whatswrong_tmp_tst')
            f = file(path, 'w')
            f.write('#!/bin/sh\necho "test"')
            f.close()
            os.chmod(path, 0755)
            res = tools.cmd(path)
            if 'test' in res['stdout']:
                results.append(tmp_dir)
        except IOError, e:
            pass

    if results:
        return (scanner.FAIL, 'Executable files possible in tmp dirs: %s' % (', '.join(results)))
    else:
        return (scanner.PASS, 'No executables possible in tmp dirs')

