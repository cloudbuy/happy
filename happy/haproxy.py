#
# happy/rest.py
#
# Authors:
#   2012 Damien Churchill <damien.churchill@ukplc.net>
#
# Copyright:
#   2012 @UK Plc (c)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.    If not, write to:
#   The Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor
#   Boston, MA    02110-1301, USA.
#

import csv
import time
import socket

from cStringIO import StringIO

STATS_FIELDS = [
    'pxname','svname','qcur','qmax','scur','smax','slim','stot','bin','bout','dreq','dresp',
    'ereq','econ','eresp','wretr','wredis','status','weight','act','bck','chkfail','chkdown',
    'lastchg','downtime','qlimit','pid','iid','sid','throttle','lbtot','tracked','type',
    'rate','rate_lim','rate_max','check_status','check_code','check_duration','hrsp_1xx',
    'hrsp_2xx','hrsp_3xx','hrsp_4xx','hrsp_5xx','hrsp_other','hanafail','req_rate',
    'req_rate_max','req_tot','cli_abrt','srv_abrt'
]

NUMERIC_FIELDS = [

]

class HAProxy(object):

    def __init__(self, path):
        self.path = path

    def execute(self, command, extra='', timeout=200):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        buf = StringIO()
        end = time.time() + timeout

        if extra:
            command = command + ' ' + extra

        try:
            s.connect(self.path)
            s.send(command + '\n')

            while time.time() <= end:
                data = s.recv(4096)
                if data:
                    buf.write(data)
                else:
                    buf.seek(0)
                    return buf

        finally:
            s.close()

    def clear_counters(self):
        return self.execute('clear counters').getvalue()

    def clear_all_counters(self):
        return self.execute('clear counters all').getvalue()

    def disable_server(self, backend, server):
        return self.execute('disable server %s/%s' % (backend, server)).getvalue()

    def enable_server(self, backend, server):
        return self.execute('enable server %s/%s' % (backend, server)).getvalue()

    def get_weight(self, backend, server):
        self.execute('get weight %s/%s' % (backend, server))

    def set_weight(self, backend, server, weight):
        self.execute('set weight %s/%s %s' % (backend, server, weight))

    def show_errors(self, backend=None):
        pass

    def show_info(self):
        result = self.execute('show info').getvalue()
        if not result:
            return {}

        info = {}
        for line in result.splitlines():
            line = line.strip()
            if not line:
                continue
            k, v = line.split(':', 1)
            info[k] = v.strip()
        return info

    def show_sessions(self):
        pass

    def show_stats(self, backend=None, type=None, sid=None):
        b = backend or -1
        t = type or -1
        s = sid or -1
        result = self.execute('show stat %d %d %d' % (b, t, s))
        reader = csv.DictReader(result, STATS_FIELDS, 'junk')
        reader.next() # skip junk header
        return list(reader)
