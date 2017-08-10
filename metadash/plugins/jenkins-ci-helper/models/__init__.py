"""
Example Plugin, also used for testing and debug
"""
import requests
from metadash.event import on
from metadash.async import deferred, debounce
from metadash.injector import require


testrun = require('testrun')


@on(testrun, 'after_save')
@deferred
@debounce(5)
def fetch_testrun_console_text(mapper, connection, target):
    if target.status == 'FINISHED':
        ref_url = ''.join(target.ref_url.split('#')[:-1]).rstrip('/')
        if ref_url:
            res = requests.get('{}/consoleText'.format(ref_url))
            if res.status_code == requests.codes.ok:
                target.details['console_text'] = res.text
            else:
                target.details['console_text'] = "Failed retriving console log with %s" % res.text
