whatswrong
==========

whatswrong scans your system for misconfigurations, security problems and other
issues. It is a whitebox scan, which means it catches more issues than can be
found with a blackbox scan. It scans system settings, application
configurations, security problems, virtual machine problems, best-practices,
etc. 

It presents the user with a report that includes severity, impact to fix, cost
to fix and an explanation of the problem. New scans can easily be added to the
system, and the scanner requires nothing by Python v2.6+, which should be
available on most systems.

Example output for the console:

    [fboender@zoltar]~/src$ ./whatswrong.py 
    Pass  Severity  Impact  CostToFix  Item                 Msg
    pass  3         1       1          web::powered_by      The webserver does
    pass  4         2       1          sys::ntpd            NTPd is running
    n/a   5         3       1          web::ssl::v3         Can't test for SSL
    pass  3         3       1          mysql::no_root_pw    The MySQL root acc
    n/a   2         3       2          sys::vm::agent       This doesn't appea
    pass  5         2       1          ssh::empty_passwords The SSH server doe
    pass  4         4       1          ssh::root_login      SSH does not allow
    err   5         4       1          php::display_errors  Scan error: [Errno
    fail  3         3       4          sys::tmp::executable Executable files p
    n/a   5         3       1          web::ssl::v2         Can't test for SSL
    pass  3         1       1          web::server_banner   The webserver does

For convenience' sake, the whole of Whatswrong can be downloaded as a single
.zip file, which can immediately be run by Python.


Usage
-----

    Usage: whatswrong.py [options] [scan pattern]

    Options:
      -h, --help   show this help message and exit
      -d, --debug  Show debugging info

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

