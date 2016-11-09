import os
import scanner

output_map = {
    scanner.PASS: {
        'title': 'pass',
        'color_console': '\033[92m',
        'color_rgb': '#40FF40',
    },
    scanner.FAIL: {
        'title': 'fail',
        'color_console': '\033[91m',
        'color_rgb': '#FF4040',
    },
    scanner.NA: {
        'title': 'n/a',
        'color_console': '\033[94m',
        'color_rgb': '#4040FF',
    },
    scanner.ERROR: {
        'title': 'err',
        'color_console': '\033[95m',
        'color_rgb': '#FFFF40',
    },
    scanner.UNKNOWN: {
        'title': '????',
        'color_console': '',
        'color_rgb': '',
    }
}


class Output:
    def __init__(self, results, show):
        self.show = show
        self.raw_results = results
        self.results = map(self._apply_result, filter(self._should_show, results))

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

        for result in self.results:
            show_cols = cols
            if os.isatty(1):
                color_start = result['color_console']
                color_end = end_color
                show_cols += 8 # Compensate for ANSI escape seq
            else:
                color_start = ''
                color_end = ''

            line = "%s%-4s%s  %s         %s       %s          %-*s %s" % (
                color_start,
                result['status_title'],
                color_end,
                result['severity'],
                result['impact'],
                result['cost_to_fix'],
                longest_ident,
                result['ident'],
                result['msg'],
            )
            print line[:show_cols]

    def tab(self):
        '''
        Output machine-readable (tab-seperated) format.
        '''
        inc_fields = ['status_title', 'status', 'impact', 'ident', 'severity',
                      'cost_to_fix', 'msg']
        print '\t'.join(inc_fields)
        for result in self.results:
            print '\t'.join([str(result[k]) for k in inc_fields])

    def json(self):
        '''
        Output results in JSON format.
        '''
        import json

        inc_fields = ['status_title', 'status', 'impact', 'ident', 'severity',
                      'cost_to_fix', 'msg', 'explanation']
        results = []
        for result in self.results:
            filtered_result = dict([ (k, v) for k, v in result.items() if k in inc_fields ])
            results.append(filtered_result)
        print json.dumps(results)

    def csv(self):
        '''
        Output results in CSV format.
        '''
        import StringIO
        import csv

        fieldnames = ['status_title', 'impact', 'ident', 'severity', 'cost_to_fix',
                      'msg', 'explanation', 'status']
        f = StringIO.StringIO()
        w = csv.DictWriter(f, fieldnames, extrasaction='ignore')
        w.writerow(dict( (k, k) for k in fieldnames ))
        for result in self.results:
            w.writerow(result)

        f.seek(0)
        print f.read()
        f.close()

    def html(self):
        import textwrap
        html_header = textwrap.dedent('''
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="UTF-8">
            <title>Scan results</title>
            <style>
                * { font-family: sans-serif; font-size: 0.95em; }
                table { border-collapse: collapse; margin-bottom: 32px; }
                tr { border-bottom: 1px solid #C0C0C0; }
                th { text-align: left; vertical-align: top; }

            </style>
            </head>
            <body>
            ''')
        html_footer = textwrap.dedent('''
            </body>
            </html>
        ''')
        html_entry = textwrap.dedent('''
            <table width="550px">
                <tbody>
                    <tr><td colspan="2">%(msg)s</td></tr>
                    <tr><th>Status</th><td><font color="%(color_rgb)s">%(status_title)s</font></td></tr>
                    <tr><th>Impact</th><td>%(impact)s</td></tr>
                    <tr><th>ident</th><td>%(ident)s</td></tr>
                    <tr><th>Severity</th><td>%(severity)s</td></tr>
                    <tr><th>Cost to fix</th><td>%(cost_to_fix)s</td></tr>
                    <tr><th>Explanation</th><td>%(explanation)s</td></tr>
                </tbody>
            </table>
        ''')
        print html_header
        for result in self.results:
            print html_entry % result
        print html_footer

    def _should_show(self, result):
        '''
        Returns True if the user requested to see results of this type. False
        otherwise
        '''
        # Skip results the user doesn't want to see.
        status_title = output_map[result['status']]['title']
        return status_title in self.show

    def _apply_result(self, result):
        '''
        '''
        clean_result = result.copy()

        for k, v in clean_result.items():
            # Remove entries starting with an underscore. They are private, and
            # the JSON export can't handle certain values in the result
            # (_module).
            if k.startswith('_'):
                del clean_result[k]

            # Remove newlines
            clean_result['explanation'] = ' '.join(clean_result['explanation'].split('\n'))

            # Map the output_map values onto the result.
            clean_result.update(output_map[result['status']])

            # Translate status to human-readable
            clean_result['status_title'] = output_map[result['status']]['title']

        return clean_result
