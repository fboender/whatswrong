import os

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
