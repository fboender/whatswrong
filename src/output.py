import os
import scanner
import json

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
    def __init__(self, results, show):
        self.results = results
        self.show = show

    def console(self):
        '''
        Output results in console format.
        '''
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

        for result in filter(self._should_show, self.results):
            status_title = output_map[result['status']]['title']
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
                status_title,
                color_end,
                result['severity'],
                result['impact'],
                result['cost_to_fix'],
                longest_ident,
                result['ident'],
                result['msg'],
            )
            print line[:show_cols]

    def json(self):
        '''
        Output results in JSON format.
        '''
        results = []
        for result in filter(self._should_show, self.results):
            results.append(self._clean_result(result))
        print json.dumps(results)

    def csv(self):
        print 'csv'

    def _should_show(self, result):
        '''
        Returns True if the user requested to see results of this type. False
        otherwise
        '''
        # Skip results the user doesn't want to see.
        status_title = output_map[result['status']]['title']
        return status_title in self.show

    def _clean_result(self, result):
        '''
        Return a cleaned up result for use in JSON and CSV output.
        '''
        clean_result = result.copy()

        for k, v in clean_result.items():
            # Remove entries starting with an underscore
            if k.startswith('_'):
                del clean_result[k]

            # Remove newlines
            clean_result['explanation'] = ' '.join(clean_result['explanation'].split('\n'))

        return clean_result
