#
# hapi/views.py
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

from hapi.config import Config
from hapi.haproxy import HAProxy
from hapi.rest import get, post, put

haproxy = HAProxy('/run/haproxy.sock')

@get('/backends')
def list_backends(**opts):
    cfg = Config('/etc/haproxy/haproxy.cfg')
    cfg.load()

    backends = []
    for bck in (b for b in cfg if b.keyword in ('listen', 'backend')):
        servers = []
        for server in (s[1] for s in bck.keywords if s[0] == 'server'):
            servers.append({
                'name': server[0],
                'address': server[1]
            })
        backends.append({
            'name': bck.name,
            'listen': bck.options[0],
            'servers': servers
        })
    return backends

@get('/backends/:backend')
def get_backend(**opts):
    cfg = Config('/etc/haproxy/haproxy.cfg')
    cfg.load()

@get('/backends/:backend/servers/:server/:action')
def action_server(**opts):
    if opts.get('action') not in ('enable', 'disable'):
        raise ValueError('Unknown action: ' + opts.get('action'))

    if opts.get('action') == 'enable':
        method = haproxy.enable_server
    else:
        method = haproxy.disable_server

    method(opts.get('backend'), opts.get('server'))
