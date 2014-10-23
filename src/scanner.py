import zipfile
import os
import imp
import re
import traceback
import sys

PASS = 1
FAIL = 2
ERROR = 3
NA = 4
UNKNOWN = 5

class ScanError(Exception):
    pass

class Scanner:
    def __init__(self, debug=False):
        self.scans = {}
        self.debug = debug
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
            'status': UNKNOWN,
        }
        result.update(scan)
        try:
            res = callback()
            if not res or len(res) != 2:
                raise ScanError("Invalid results received from scanner: %s" % (ident))
            scan_result, msg = res
            result['status'] = scan_result
            result['msg'] = msg
        except ScanError, e:
            result['status'] = ERROR
            result['msg'] = 'Scan error: %s' % (str(e))
            if self.debug:
                traceback.print_exc()
        except Exception, e:
            result['status'] = ERROR
            result['msg'] = 'Scan error: %s' % (str(e))
            if self.debug:
                traceback.print_exc()

        return result

class ScannerSrc(Scanner):
    def __init__(self, dir, debug=False):
        self.dir = dir
        Scanner.__init__(self, debug)

    def load_scans(self):
        for fname in os.listdir(self.dir):
            if fname.endswith('.py'):
                try:
                    modname = fname.split('.')[0]
                    scanmodule = imp.load_source(modname, os.path.join(self.dir, fname))
                    scan_info = {
                        'ident': scanmodule.__ident__,
                        'severity': scanmodule.__severity__,
                        'impact': scanmodule.__impact__,
                        'cost_to_fix': scanmodule.__cost_to_fix__,
                        #'fail_msg': scanmodule.__fail_msg__,
                        'explanation': scanmodule.__explanation__,
                        '_module': scanmodule,
                    }
                    self.scans[scanmodule.__ident__] = scan_info
                except Exception, e:
                    sys.stderr.write("Couldn't load scan '%s': %s\n" % (fname, e))

class ScannerZip(Scanner):
    def __init__(self, zip, debug=False):
        self.zip = zip
        Scanner.__init__(self, debug)

    def load_scans(self):
        z = zipfile.ZipFile(self.zip, 'r')
        for fname in z.namelist():
            if fname.startswith('scans/') and fname.endswith('.py'):
                try:
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
                        #'fail_msg': scanmodule.__fail_msg__,
                        'explanation': scanmodule.__explanation__,
                        '_module': scanmodule,
                    }
                    self.scans[scanmodule.__ident__] = scan_info
                except Exception, e:
                    sys.stderr.write("Couldn't load scan '%s': %s\n" % (fname, e))
        z.close()
