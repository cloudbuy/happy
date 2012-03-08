#
# happy/config.py
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

import os

class Config(object):

    def __init__(self, filename):
        self.fn = filename
        self.sections = []

    def __iter__(self):
        return iter(self.sections)

    def load(self):
        fp = open(self.fn)
        length = os.fstat(fp.fileno()).st_size

        section = None
        while fp.tell() < length:
            line = fp.readline().rstrip()

            if not line.strip():
                continue

            if line.strip().startswith('#'):
                continue

            if line[0].isspace() and section:
                section.parseline(line.strip())
            else:
                parts = line.split()
                if parts[0] not in SECTIONS:
                    raise Exception('Unsupported configuration section: %s' % parts[0])
                section = SECTIONS[parts[0]](*parts[1:])
                self.sections.append(section)

class BaseSection(object):

    keyword        = None
    VALID_KEYWORDS = None

    def __init__(self, *args, **kwargs):
        self.options = args
        self.keywords = []

    def parseline(self, line):
        parts = line.split()

        keyword = parts[0]
        valid   = False
        if keyword not in self.VALID_KEYWORDS:
            for i in xrange(1, len(parts)):
                keyword += (' ' + parts[i])
                if keyword in self.VALID_KEYWORDS:
                    valid = True
                    options = parts[i+1:]
                    break
        else:
            valid = True
            options = parts[1:]

        if not valid:
            raise Exception('Error: %s' % line)

        self.keywords.append((keyword, options))

KEYWORDS = {
    'acl': {
        'sections': ['frontend', 'listen', 'backend'],
        'args': ['aclname', 'criterion']
    },
    'appsession': {
        'sections': ['listen', 'backend'],
        'args': ['cookie']
    },
    'backlog': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'balance': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'bind': {
        'sections': ['frontend', 'listen']
    },
    'bind-process': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'block': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'capture cookie': {
        'sections': ['frontend', 'listen']
    },
    'capture request header': {
        'sections': ['frontend', 'listen']
    },
    'capture response header': {
        'sections': ['frontend', 'listen']
    },
    'chroot': {
        'sections': ['global'],
        'args': [('jail_dir', str)]
    },
    'clitimeout': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'contimeout': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'cookie': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'daemon': {
        'sections': ['global']
    },
    'debug': {
        'sections': ['global']
    },
    'default-server': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'default_backend': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'description': {
        'sections': ['global', 'frontend', 'listen', 'backend']
    },
    'disabled': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'dispatch': {
        'sections': ['listen', 'backend']
    },
    'enabled': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'errorfile': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'errorloc': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'errorloc302': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'errorloc303': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'force-persist': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'fullconn': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'gid': {
        'sections': ['global'],
        'args': [('gid', int)]
    },
    'grace': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'group': {
        'sections': ['global'],
        'args': [('group', str)]
    },
    'hash-type': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'http-check disable-on-404': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'http-request': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'id': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'ignore-persist': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'log': {
        'sections': ['global', 'defaults', 'frontend', 'listen', 'backend']
    },
    'log-send-hostname': {
        'sections': ['global']
    },
    'log-tag': {
        'sections': ['global']
    },
    'maxconn': {
        'sections': ['global', 'defaults', 'frontend', 'listen']
    },
    'maxpipes': {
        'sections': ['global']
    },
    'mode': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'monitor fail': {
        'sections': ['frontend', 'listen']
    },
    'monitor-net': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'monitor-uri': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'nbproc': {
        'sections': ['global']
    },
    'node': {
        'sections': ['global']
    },
    'noepoll': {
        'sections': ['global']
    },
    'nokqueue': {
        'sections': ['global']
    },
    'nopoll': {
        'sections': ['global']
    },
    'nosepoll': {
        'sections': ['global']
    },
    'nosplice': {
        'sections': ['global']
    },
    'option abortonclose': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'option accept-invalid-http-request': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'option accept-invalid-http-response': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'option allbackups': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'option checkcache': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'option clitcpka': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'option contstats': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'option dontlog-normal': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'option dontlognull': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'option forceclose': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'option forwardfor': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'option http-pretend-keepalive': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'option http-server-close': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'option http-use-proxy-header': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'option http_proxy': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'option httpchk': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'option httpclose': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'option httplog': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'option independant-streams': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'option log-health-checks': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'option log-separate-errors': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'option logasap': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'option mysql-check': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'option nolinger': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'option originalto': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'option persist': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'option redispatch': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'option smtpchk': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'option socket-stats': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'option splice-auto': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'option splice-request': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'option splice-response': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'option srvtcpka': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'option ssl-hello-chk': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'option tcp-smart-accept': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'option tcp-smart-connect': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'option tcpka': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'option tcplog': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'option transparent': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'persist rdp-cookie': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'pidfile': {
        'sections': ['global']
    },
    'quiet': {
        'sections': ['global']
    },
    'rate-limit sessions': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'redirect': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'redisp': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'redispatch': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'reqadd': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'reqallow': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'reqdel': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'reqdeny': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'reqiallow': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'reqidel': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'reqideny': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'reqipass': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'reqirep': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'reqisetbe': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'reqitarpit': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'reqpass': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'reqrep': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'reqsetbe': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'reqtarpit': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'retries': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'rspadd': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'rspdel': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'rspdeny': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'rspidel': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'rspideny': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'rspirep': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'rsprep': {
        'sections': ['frontend', 'listen', 'backend']
    },
    'server': {
        'sections': ['listen', 'backend'],
        'args': [('name', str), ('addr', str)]
    },
    'source': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'spread-checks': {
        'sections': ['global']
    },
    'srvtimeout': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'stats admin': {
        'sections': ['listen', 'backend']
    },
    'stats auth': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'stats enable': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'stats hide-version': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'stats maxconn': {
        'sections': ['global']
    },
    'stats realm': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'stats refresh': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'stats scope': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'stats show-desc': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'stats show-legends': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'stats show-node': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'stats socket': {
        'sections': ['global']
    },
    'stats timeout': {
        'sections': ['global']
    },
    'stats uri': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'stick match': {
        'sections': ['listen', 'backend']
    },
    'stick on': {
        'sections': ['listen', 'backend']
    },
    'stick store-request': {
        'sections': ['listen', 'backend']
    },
    'stick-table': {
        'sections': ['listen', 'backend']
    },
    'tcp-request content accept': {
        'sections': ['frontend', 'listen']
    },
    'tcp-request content reject': {
        'sections': ['frontend', 'listen']
    },
    'tcp-request inspect-delay': {
        'sections': ['frontend', 'listen']
    },
    'timeout check': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'timeout client': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'timeout clitimeout': {
        'sections': ['defaults', 'frontend', 'listen']
    },
    'timeout connect': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'timeout contimeout': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'timeout http-keep-alive': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'timeout http-request': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'timeout queue': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'timeout server': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'timeout srvtimeout': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'timeout tarpit': {
        'sections': ['defaults', 'frontend', 'listen', 'backend']
    },
    'transparent': {
        'sections': ['defaults', 'listen', 'backend']
    },
    'tune.bufsize': {
        'sections': ['global']
    },
    'tune.chksize': {
        'sections': ['global']
    },
    'tune.maxaccept': {
        'sections': ['global']
    },
    'tune.maxpollevents': {
        'sections': ['global']
    },
    'tune.maxrewrite': {
        'sections': ['global']
    },
    'tune.rcvbuf.client': {
        'sections': ['global']
    },
    'tune.rcvbuf.server': {
        'sections': ['global']
    },
    'tune.sndbuf.client': {
        'sections': ['global']
    },
    'tune.sndbuf.server': {
        'sections': ['global']
    },
    'uid': {
        'sections': ['global']
    },
    'ulimit-n': {
        'sections': ['global']
    },
    'use_backend': {
        'sections': ['frontend', 'listen']
    },
    'user': {
        'sections': ['global']
    },
}

class ProxySection(BaseSection):

    def __init__(self, name=None, *args):
        super(ProxySection, self).__init__(*args)
        self.name = name

class GlobalSection(BaseSection):
    keyword = 'global'

class DefaultsSection(ProxySection):
    keyword = 'defaults'

class FrontendSection(ProxySection):
    keyword = 'frontend'

class ListenSection(ProxySection):
    keyword = 'listen'

class BackendSection(ProxySection):
    keyword = 'backend'

SECTIONS = {c.keyword: c for c in BaseSection.__subclasses__()}
SECTIONS.update({c.keyword: c for c in ProxySection.__subclasses__()})
for kw, opts in KEYWORDS.iteritems():
    for section in opts['sections']:
        if SECTIONS[section].VALID_KEYWORDS is None:
            SECTIONS[section].VALID_KEYWORDS = {}
        SECTIONS[section].VALID_KEYWORDS[kw] = opts
