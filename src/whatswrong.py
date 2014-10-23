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
import zipfile

import scanner
import output

usage = "usage: %prog [options] [scan pattern]"
parser = optparse.OptionParser(usage)
parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False, help="Show debugging info")
parser.add_option("-s", "--show", action="store", dest="show", default='err,fail', help="Which results to show")
parser.add_option("-a", "--show-all", action="store_true", dest="show_all", default=False, help="Show all results")
(options, args) = parser.parse_args()

if len(args) < 1:
    scan_pattern = '.*'
else:
    scan_pattern = args[0]

if options.show_all:
    options.show = ['pass', 'n/a', 'fail', 'err', '????']
else:
    options.show = [v.strip() for v in options.show.split(',')]

try:
    scanner = scanner.ScannerZip(sys.argv[0], debug=options.debug)
except zipfile.BadZipfile:
    scanner = scanner.ScannerSrc('scans', debug=options.debug)

results = scanner.scan(scan_pattern)
output = output.Output(results, show=options.show)
output.console()

