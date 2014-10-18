import os
import scanner

output_map = {
    scanner.PASS: {
        'title': 'pass',
        'color_console': '\033[92m',
    },
    scanner.FAIL: {
        'title': 'fail',
        'color_console': '\033[91m',
    },
    scanner.NA: {
        'title': 'n/a',
        'color_console': '\033[94m',
    },
    scanner.ERROR: {
        'title': 'err',
        'color_console': '\033[93m',
    },
    scanner.UNKNOWN: {
        'title': '????',
        'color_console': '',
    }
}



class Output:
    def __init__(self, results):
        self.results = results

    def console(self):
        end_color = '\033[0m'
        cols = None

        if os.isatty(1):
            cols = os.environ.get('COLUMNS', None)
            try:
                r, c = os.popen('stty size', 'r').read().split()
                cols = int(c)
            except Exception:
                pass

        if not self.results:
            print "No results. You probably specified an incorrect scan."
            return

        longest_ident = max([len(s['ident']) for s in self.results])
        print 'Pass  Severity  Impact  CostToFix  %-*s Msg' % (longest_ident, 'Item')

        for result in self.results:
            show_cols = cols
            if os.isatty(1):
                color_start = output_map[result['status']]['color_console']
                color_end = end_color
                show_cols += 8 # Compensate for ANSI escape seq
            else:
                color_start = ''
                color_end = ''

            line = "%s%-4s%s  %s         %s       %s          %-*s %s" % (
                color_start,
                output_map[result['status']]['title'],
                color_end,
                result['severity'],
                result['impact'],
                result['cost_to_fix'],
                longest_ident,
                result['ident'],
                result['msg'],
            )
            print line[:show_cols]

    def csv(self):
        print 'csv'
