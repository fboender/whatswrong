import zipfile
import os
import imp
import re

class ScanError(Exception):
    pass

class Scanner:
    def __init__(self):
        self.scans = {}
        self.load_scans()

    def scan(self, scan_pattern='*'):
        scan_pattern = scan_pattern.replace('*', '.*')
        results = []
        for scan in self.scans.keys():
            if re.match(scan_pattern, scan):
                results.append(self.run(scan))
        return results

    def run(self, ident):
        try:
            scan = self.scans[ident]
        except KeyError:
            raise ScanError("Unknown scan: %s" % (ident))

        callback = scan['_module'].scan
        result = {
            'status': '????'
        }
        result.update(scan)
        try:
            res = callback()
            if res == True:
                result['status'] = 'fail'
            elif res == False:
                result['status'] = 'pass'
            else:
                result['status'] = 'n/a'
        except ScanError, e:
            result['status'] = 'err'
            result['fail_msg'] = 'Test failed: %s' % (str(e))
        except Exception, e:
            result['status'] = 'err '
            result['fail_msg'] = 'Test failed: %s' % (str(e))

        return result

class ScannerSrc(Scanner):
    def __init__(self, dir):
        self.dir = dir
        Scanner.__init__(self)

    def load_scans(self):
        for fname in os.listdir(self.dir):
            if fname.endswith('.py'):
                modname = fname.split('.')[0]
                scanmodule = imp.load_source(modname, os.path.join(self.dir, fname))
                scan_info = {
                    'ident': scanmodule.__ident__,
                    'severity': scanmodule.__severity__,
                    'impact': scanmodule.__impact__,
                    'cost_to_fix': scanmodule.__cost_to_fix__,
                    'fail_msg': scanmodule.__fail_msg__,
                    'explanation': scanmodule.__explanation__,
                    '_module': scanmodule,
                }
                self.scans[scanmodule.__ident__] = scan_info

class ScannerZip(Scanner):
    def __init__(self, zip):
        self.zip = zip
        Scanner.__init__(self)

    def load_scans(self):
        z = zipfile.ZipFile(self.zip, 'r')
        for fname in z.namelist():
            if fname.startswith('scans/') and fname.endswith('.py'):
                f = z.open(fname)
                fc = f.read()
                modname = fname.split('.')[0]
                scanmodule = imp.new_module(modname)
                exec fc in scanmodule.__dict__

                scan_info = {
                    'ident': scanmodule.__ident__,
                    'severity': scanmodule.__severity__,
                    'impact': scanmodule.__impact__,
                    'cost_to_fix': scanmodule.__cost_to_fix__,
                    'fail_msg': scanmodule.__fail_msg__,
                    'explanation': scanmodule.__explanation__,
                    '_module': scanmodule,
                }
                self.scans[scanmodule.__ident__] = scan_info
        z.close()
