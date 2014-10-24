import scanner

__ident__ = 'sys::tmp::mount'
__severity__ = 2
__impact__ = 1
__cost_to_fix__ = 5
__explanation__ = '''Temporary directories with global write access should be
mounted on a separate volume to prevent users from filling the filesystem and
interfering with the normal operation of the system'''

def scan():
    for line in file('/proc/mounts', 'r'):
        if line.split()[1] == '/tmp':
            return (scanner.PASS, '/tmp is mounted separately')
    return (scanner.FAIL, '/tmp is not mounted separately')
