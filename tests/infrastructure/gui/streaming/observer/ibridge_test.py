# -*- coding: UTF-8 -*-

'''
Module
    ibridge_test.py
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
    Unit tests for IGuiStreamObserverBridge interface and protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.telemetry.progress import StreamProgress
from scarajectory.infrastructure.gui.streaming.observer.ibridge import IGuiStreamObserverBridge

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingBridgeStub:
    '''
        Conforming stub implementation satisfying IGuiStreamObserverBridge.

        It defines:

            :methods:
                | on_stream_progress - Simulates stream progress event.
                | on_serial_log - Simulates serial log event.
    '''

    def on_stream_progress(self, progress: StreamProgress) -> None:
        '''
            Simulates stream progress event.

            :param progress: StreamProgress metric container.
            :exceptions: None.
        '''
        del progress

    def on_serial_log(self, text: str, is_outgoing: bool = False) -> None:
        '''
            Simulates serial log event.

            :param text: Message string content.
            :param is_outgoing: Flag indicating outgoing direction.
            :exceptions: None.
        '''
        del text, is_outgoing


class TestIGuiStreamObserverBridge(TestCase):
    '''
        Tests verifying IGuiStreamObserverBridge protocol definition and subtyping.

        It defines:

            :methods:
                | test_protocol_methods - Verifies methods declared on protocol.
                | test_conforming_stub_subtyping - Verifies stub satisfies protocol.
    '''

    def test_protocol_methods(self) -> None:
        '''
            Verifies methods declared on IGuiStreamObserverBridge protocol.

            :exceptions: None.
        '''
        self.assertTrue(hasattr(IGuiStreamObserverBridge, 'on_stream_progress'))
        self.assertTrue(hasattr(IGuiStreamObserverBridge, 'on_serial_log'))

    def test_conforming_stub_subtyping(self) -> None:
        '''
            Verifies conforming stub satisfies IGuiStreamObserverBridge structurally.

            :exceptions: None.
        '''
        stub = ConformingBridgeStub()
        self.assertIsInstance(stub, IGuiStreamObserverBridge)


if __name__ == '__main__':
    main()
