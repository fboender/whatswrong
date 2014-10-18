import re
import tools

__ident__ = 'sys::vm::agent'
__severity__ = 2
__impact__ = 3
__cost_to_fix__ = 2
__fail_msg__ = 'No agent running on this virtual machine'
__explanation__ = ''

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
                return True
            else:
                return False
    return None
