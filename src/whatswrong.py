#!/usr/bin/python

#
# TODO:
#  - Firewall: enabled, incoming, outgoing
#  - Kernel: dangerous options enabled
#  - SSL: v2 / v3 enabled: Needs fixing
#  - Sys: tmp dirs executable
#  - All ips / hostnames in /etc/hosts
#  - ROot email delivered
#  - Cron email delivered
#  - fail2ban
#  - MySQL: listen port, users

import sys
import optparse
import imp
import zipfile
import os
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
            result['err_msg'] = 'Test failed: %s' % (str(e))
        except Exception, e:
            result['status'] = 'err '
            result['err_msg'] = 'Test failed: %s' % (str(e))

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

class Output:
    def __init__(self, results):
        self.results = results

    def console(self):
        color_map = {
            'pass': '\033[92m',
            'fail': '\033[91m',
            'n/a': '\033[94m',
            'err ': '\033[93m',
        }
        end_color = '\033[0m'

        if not self.results:
            print "No results. You probably specified an incorrect scan."
            return

        longest_ident = max([len(s['ident']) for s in self.results])
        print 'Pass  Severity  Impact  CostToFix  %-*s Msg' % (longest_ident, 'Item')

        for result in self.results:
            if os.isatty(1):
                color_start = color_map[result['status']]
                color_end = end_color
            else:
                color_start = ''
                color_end = ''

            print "%s%-4s%s  %s         %s       %s          %-*s %s" % (
                color_start,
                result['status'],
                color_end,
                result['severity'],
                result['impact'],
                result['cost_to_fix'],
                longest_ident,
                result['ident'],
                result['fail_msg'],
            )

    def csv(self):
        print 'csv'

usage = "usage: %prog [options] [scan pattern]"
parser = optparse.OptionParser(usage)
#parser.add_option("-V", "--verbose", action="store_true", dest="verbose", default=False, help="Log verbose info")
(options, args) = parser.parse_args()

if len(args) < 1:
    scan_pattern = '.*'
else:
    scan_pattern = args[0]

try:
    scanner = ScannerZip(sys.argv[0])
except zipfile.BadZipfile:
    scanner = ScannerSrc('scans')

results = scanner.scan(scan_pattern)
output = Output(results)
output.console()

