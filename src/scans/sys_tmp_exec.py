import scanner
import tools
import os

__ident__ = 'sys::tmp::executable'
__severity__ = 3
__impact__ = 3
__cost_to_fix__ = 4
__explanation__ = '''Many rootkits and automated exploits use the system's
temporary dirs to execute programs that exploit your system. To prevent this,
temp directories should not allow the execution of temp files.'''

def scan():
    tmp_dirs = [
        '/tmp',
        '/var/tmp',
    ]

    result = scanner.Result()
    for tmp_dir in tmp_dirs:
        path = os.path.join(tmp_dir, 'whatswrong_tmp_tst')
        try:
            f = file(path, 'w')
            f.write('#!/bin/sh\necho "test"')
            f.close()
            os.chmod(path, 0755)
            res = tools.cmd(path)
            if 'test' in res['stdout']:
                result.add(scanner.FAIL, 'Executable files possible in: %s' % tmp_dir)
        except IOError, e:
            pass
        if os.path.exists(path):
            os.unlink(path)

    if result:
        return result
    else:
        return scanner.Result(scanner.PASS, 'No executables possible in tmp dirs')
