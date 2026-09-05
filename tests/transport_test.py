# -*- coding: UTF-8 -*-

'''
Module
    transport_test.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    scarajectory is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    scarajectory is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Unit tests for SerialTransport, TcpTransport, and SerialStreamer.
'''

from __future__ import annotations

import os
import sys
import unittest

pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)

from scarajectory.infrastructure.communication.transport.serial_transport import SerialTransport
from scarajectory.infrastructure.communication.transport.tcp_transport import TcpTransport
from scarajectory.infrastructure.communication.serial_streamer import SerialStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTransport(unittest.TestCase):
    '''
        Test cases for Transport layers and Streamer lifecycle.

        It defines:

            :methods:
                | test_serial_transport_initial_state - Tests default properties of SerialTransport.
                | test_tcp_transport_initial_state - Tests default properties of TcpTransport.
                | test_streamer_lifecycle - Tests SerialStreamer creation and control flags.
    '''

    def test_serial_transport_initial_state(self) -> None:
        '''
            Tests initial state of SerialTransport.

            :exceptions: None.
        '''
        transport = SerialTransport()
        self.assertFalse(transport.is_connected())
        transport.disconnect()
        self.assertFalse(transport.is_connected())

    def test_tcp_transport_initial_state(self) -> None:
        '''
            Tests initial state of TcpTransport.

            :exceptions: None.
        '''
        transport = TcpTransport()
        self.assertFalse(transport.is_connected())
        transport.disconnect()
        self.assertFalse(transport.is_connected())

    def test_streamer_lifecycle(self) -> None:
        '''
            Tests SerialStreamer creation and control flags.

            :exceptions: None.
        '''
        transport = SerialTransport()
        streamer = SerialStreamer(transport)
        self.assertFalse(streamer.is_connected())

        streamer.pause_streaming()
        streamer.resume_streaming()
        streamer.stop_streaming()


if __name__ == '__main__':
    unittest.main()
