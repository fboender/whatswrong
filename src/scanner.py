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

class Result:
    def __init__(self, status=None, msg=None):
        self.results = []
        if status:
            self.results.append( (status, msg) )

    def add(self, status, msg):
        self.results.append( (status, msg) )

    def __nonzero__(self):
        if self.results:
            return True
        else:
            return False

    def __iter__(self):
        for result in self.results:
            yield result

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
                for result in self.run_scan(scan):
                    results.append(result)
        return results

    def run_scan(self, ident):
        try:
            scan = self.scans[ident]
            callback = scan['_module'].scan
        except KeyError:
            raise ScanError("Unknown scan: %s" % (ident))

        scan_results = []
        try:
            r = callback()
            if not isinstance(r, Result):
                raise Exception('Scanner returned invalid results')
            for result_status, result_msg in r:
                result = {
                    'status': result_status,
                    'msg': result_msg
                }
                result.update(scan)
                scan_results.append(result)
        except Exception, e:
            result = {
                'status': ERROR,
                'msg': 'Scan error: %s' % (str(e))
            }
            result.update(scan)
            scan_results.append(result)
            if self.debug:
                traceback.print_exc()

        return scan_results


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
