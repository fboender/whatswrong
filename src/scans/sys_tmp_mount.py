import scanner
import os

__ident__ = 'sys::tmp::mount'
__severity__ = 2
__impact__ = 1
__cost_to_fix__ = 5
__explanation__ = '''Temporary directories with global write access should be
mounted on a separate volume to prevent users from filling the filesystem and
interfering with the normal operation of the system'''

def scan():
    tmp_dirs = [
        '/tmp',
        '/var/tmp',
    ]

    result = scanner.Result()
    for tmp_dir in tmp_dirs:
        if not os.path.isdir(tmp_dir):
            continue

        tmp_dir_found = False
        for line in file('/proc/mounts', 'r'):
            if line.split()[1] == tmp_dir:
                tmp_dir_found = True
        if tmp_dir_found:
            result.add(scanner.PASS, '%s is mounted separately' % tmp_dir)
        else:
            result.add(scanner.FAIL, '%s is not mounted separately' % tmp_dir)
    return result
