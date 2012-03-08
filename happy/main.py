#
# happy/main.py
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

from argparse import ArgumentParser
from happy.rest import WebServer

import happy.views

def main():
    server = WebServer(9876, True, True)
    server.start()
