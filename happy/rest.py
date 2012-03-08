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

#from gevent import monkey; monkey.patch_all()

import json
import bottle
import collections

ENCODERS = {}

Encoder = collections.namedtuple('Encoder', 'encoder decoder ctype')

def decode_json(data):
    try:
        return json.loads(data)
    except TypeError:
        return json.load(data)

def encode_json(data):
    return json.dumps(data)

ENCODERS['json'] = Encoder(encode_json, decode_json, 'application/json')

def route(path, method='GET', callback=None, **options):
    if callable(path): path, callback = None, path
    def deco(func):
        def wrapper(**urlargs):
            fmt = urlargs.pop('fmt') if 'fmt' in urlargs else 'json'
            if fmt not in ENCODERS:
                raise Exception('Unsupported encoding')
            encoder = ENCODERS[fmt]

            # Handle older bottle versions
            try:
                urlargs.update(bottle.request.query)
            except AttributeError:
                urlargs.update(bottle.request.GET)

            if method in ('POST', 'PUT'):
                data = encoder.decode(bottle.request.body)
                result = func(data, **urlargs)
            else:
                result = func(**urlargs)

            bottle.response.set_header('Content-Type', encoder.ctype)

            return encoder.encoder(result)

        bottle.route(path, method, wrapper, **options)
        bottle.route(path + '.:fmt', method, wrapper, **options)
        return func
    return deco(callback) if callback else deco

def get(path, callback=None, **options):
    return route(path, callback=callback, **options)

def delete(path, callback=None, **options):
    return route(path, method='DELETE', callback=callback, **options)

def post(path, callback=None, **options):
    return route(path, method='POST', callback=callback, **options)

def put(path, callback=None, **options):
    return route(path, method='PUT', callback=callback, **options)

class WebServer(object):

    def __init__(self, port, debug=False, reloader=False):
        self.port     = port
        self.debug    = debug
        self.reloader = reloader

    def start(self):
        bottle.debug(self.debug)
        bottle.run(reloader=self.reloader, port=self.port, server='gevent')
