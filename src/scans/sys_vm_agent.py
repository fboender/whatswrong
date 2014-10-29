import scanner
import re
import tools

__ident__ = 'sys::vm::agent'
__severity__ = 2
__impact__ = 3
__cost_to_fix__ = 2
__explanation__ = '''Virtual systems should usually run a Virtual Machine agent
that lets the host system communicate and control the virtual machine more
efficiently. The absence of a VM agent may interfere with the system clock,
memory ballooning, etc'''

def scan():
    vm = False

    vm_detect_map = [
        ('lspci', '.*vmware.*', ''),
        ('lspci', '.*virtualbox.*', 'VBoxService'),
        ('lscpu', '.*xen.*', ''),
        ('lscpu', '.*microsoft.*', ''),
    ]

    for cmd, regex, agent_proc in vm_detect_map:
        res = tools.cmd(cmd)
        match = re.match(regex, res['stdout'], flags=re.IGNORECASE | re.DOTALL)
        if match:
            res_pidof = tools.cmd('pidof %s' % (agent_proc))
            if res_pidof['exitcode'] != 0:
                return scanner.Result(scanner.PASS, 'A vm agent is running')
            else:
                return scanner.Result(scanner.PASS, 'No vm agent is running')
    return scanner.Result(scanner.NA, 'This doesn\'t appear to be a vm')
