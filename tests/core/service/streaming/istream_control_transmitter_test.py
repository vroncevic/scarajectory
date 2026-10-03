# -*- coding: UTF-8 -*-

'''
Module
    istream_control_transmitter_test.py
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
    Unit testing for IStreamControlTransmitter protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.service.streaming.istream_control_transmitter import (
    IStreamControlTransmitter,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamControlTransmitterStub:
    '''Structural test stub satisfying IStreamControlTransmitter protocol.'''

    def send_enable(self, mode: ProtocolMode) -> None:
        '''Transmits enable.'''
        _ = mode

    def send_hold(self, mode: ProtocolMode) -> None:
        '''Transmits hold.'''
        _ = mode

    def send_resume(self, mode: ProtocolMode) -> None:
        '''Transmits resume.'''
        _ = mode

    def send_estop(self, mode: ProtocolMode) -> None:
        '''Transmits estop.'''
        _ = mode


class IncompleteStreamControlTransmitterStub:
    '''Incomplete test stub missing required transmitter methods.'''

    def send_enable(self, mode: ProtocolMode) -> None:
        '''Transmits enable.'''
        _ = mode

    def send_hold(self, mode: ProtocolMode) -> None:
        '''Transmits hold.'''
        _ = mode


class StreamControlTransmitterTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IStreamControlTransmitter.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IStreamControlTransmitter protocol.'''
        stub = StreamControlTransmitterStub()
        self.assertIsInstance(stub, IStreamControlTransmitter)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IStreamControlTransmitter protocol check.'''
        incomplete = IncompleteStreamControlTransmitterStub()
        self.assertNotIsInstance(incomplete, IStreamControlTransmitter)


if __name__ == '__main__':
    main()
