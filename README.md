whatswrong
==========

whatswrong scans your system for misconfigurations, security problems and other
issues. It is a whitebox scan, which means it catches more issues than can be
found with a blackbox scan. It scans system settings, application
configurations, security problems, virtual machine problems, best-practices,
etc. 

It presents the user with a report that includes severity, impact to fix, cost
to fix and an explanation of the problem. Reports can be generated on the
console, as CSV, as JSON or as HTML. New scans can easily be added to the
system, and the scanner requires nothing by Python v2.6+, which should be
available on most systems.

Example output for the console:

    [fboender@host]~$ ./whatswrong.py -a
    Pass  Severity  Impact  CostToFix  Item                 Msg
    pass  3         1       1          web::powered_by      The webserver does not exposes backend software vi
    n/a   5         3       1          web::ssl::v2         Can't test for SSLv2: _ssl.c:475: The handshake op
    n/a   5         3       1          web::ssl::v3         Can't test for SSLv3: [Errno 1] _ssl.c:490: error:
    pass  3         3       1          mysql::no_root_pw    The MySQL root account has a password
    pass  2         3       2          sys::vm::agent       No vm agent is running
    pass  3         3       1          mysql::listen        MySQL is not listening on all addresses
    fail  4         4       1          ssh::root_login      SSH allows remote root logins
    pass  5         4       1          php::display_errors  /etc/php5/apache2/php.ini does not have display_er
    fail  3         3       4          sys::tmp::executable Executable files possible in tmp dirs: /tmp, /var/
    fail  4         2       1          sys::ntpd            NTPd is not running
    fail  2         1       5          sys::tmp::mount      /tmp is not mounted separately
    pass  5         2       1          ssh::empty_passwords The SSH server does not allow empty passwords
    fail  3         1       1          web::server_banner   The webserver exposes a header with version number

For convenience' sake, the whole of Whatswrong can be downloaded as a single
.zip file, which can immediately be run by Python.

For each test, Whatswrong tells you:

* **Pass**: Whether the test passed, failed, wasn't applicable (n/a) or if an error occurred.
* **Severity**: How big of a problem this is, if the test failed. Ranges from 1
  to 5, where 5 is very severe. The higher this number, the more important it
  is to fix the problem.
* **Impact**: The potential impact on the system and services if you were to
  fix this problem. Ranges from 1 to 5, where 5 is a high potential impact and
  very likely to break something on your system if fixed.
* **CostToFix**: How much effort it would be to fix this problem. Ranges from 1
  to 5 where 1 means it's very easy to fix this problem and 5 means it's quite
  hard to fix this problem. This does **not** take in account the **impact**
  field.
* **Item**: A unique identifier for this scan. This can be used to select which
  scans you'd like to run. For instance, if you only want to run all web scans,
  specify `web::*`.
* **Msg**: A textual representation of the output of the test.


Usage
-----

Usage:

    Usage: whatswrong.py [options] [scan pattern]
   
    Options:
     -h, --help            show this help message and exit
     -d, --debug           Show debugging info
     -s SHOW, --show=SHOW  Which results to show (default: err,fail)
     -a, --show-all        Show all results
     -o OUTPUT_TYPE, --output-type=OUTPUT_TYPE
                           Output type (default: console, -o list for all
                           available)

Example:

    # Scan only all system scans.
    ./whatswrong.py sys::*

    # Run as .zip
    python ./whatswrong.zip


Adding new scans
----------------

Adding new scans is simple. Take a look at some of the other scans in the
`scans/` directory. Here's a basic scanner:

    import scanner

    __ident__ = 'example::my_example'
    __severity__ = 3
    __impact__ = 4
    __cost_to_fix__ = 1
    __explanation__ = ''

    def scan():
        res = 'FAIL'

        if res == 'FAIL':
            return (scanner.FAIL, 'The test failed: something is wrong')
        elif res == 'PASS':
            return (scanner.PASS, 'The test passed: everything is okay')
        elif res == 'ERROR_1':
            return (scanner.ERROR, 'An unexpected error occurred during the scan')
        elif res == 'ERROR_2':
            raise scanner.ScanError('An unexpected error occurred during the scan')
        elif res == 'NOT APPLICABLE':
            return (scanner.NA, 'The test did not run on purpose')
        else:
            retrun (scanner.UNKNOWN, 'Shouldn\'t be reached')

Put the file in the `scans/` directory, and Whatswrong will automatically detect it.

Scanners should return an iterable (tuple, list) with two elements:

    (STATUS_CODE, MESSAGE)

The following status codes are available:

* **`scanner.FAIL`**: The test failed, meaning something with your system is
  wrong. For instance, if you're scanning whether ntpd is installed, and it is
  not installed, you should return `scanner.FAIL`.
* **`scanner.PASS`**: The test passed, meaning everything is alright for this
  test. For instance, if you're scanning whether ntpd is installed, and it is
  installed, you should return `scanner.PASS`.
* **`scanner.ERROR`**: The scan ran into an error which caused it to not be
  able to complete the test. It is not indicative that the test passed or
  failed, but that the test did not run properly. This can be any raised
  Exception, or the scan can return the status directly if it is able to detect
  the problem. Applicable situations are not enough permissions, unexpected
  failures, missing libraries, etc. This status should *not* be returned if the
  scan *shouldn't* be run (e.g. you're scanning for PHP misconfigurations, but
  the system doesn't have PHP). In principle, the error should be fixed by the
  user and the test ran again.
* **`scanner.NA`**: Not available: The test does not apply to this system, so
  it was skipped. E.g. when you're scanning for PHP misconfigurations, but the
  system does not have PHP installed.


Things to be aware of when writing new scans:

* Scans may raise an exception, but only *inside* of the `scan()` method.
  Exceptions thrown outside the `scan()` method will prevent the test from
  running at all, giving no output or other indication that the test even
  exists. Exceptions thrown from within the `scan()` method are considered as
  scanner.ERROR cases.
* Do not use non-standard libraries. We do not want the user to have to install
  dependencies. If you *have* to use non-standard libraries, make sure to catch
  ImportErrors when importing them, and that your test returns an scanner.ERROR
  indicating that the library is not available.
* Scans are ran sequentially. Try to make tests speedy. If you're using sockets
  of any kind, set the socket timeout to a reasonable default (2 seconds).
* The returned message should match the output status of the test. E.g. if you
  return scanner.NA, the message should be something like `'Foo not
  installed'`, or for scanner.ERROR, the error message that was encountered,
  for scanner.FAIL the reason the test failed (`'A vulnerable version of bash is
  installed'`) and for scanner.PASS: `'Bash is not vulnerable'`.

