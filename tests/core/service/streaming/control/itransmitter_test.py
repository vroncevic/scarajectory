# -*- coding: UTF-8 -*-

'''
Module
    itransmitter_test.py
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
    Unit testing for IControlTransmitter structural protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.streaming.control.itransmitter import IControlTransmitter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControlTransmitterStub:
    '''Structural test stub satisfying IControlTransmitter protocol.'''

    def send_enable(self) -> None:
        '''Transmits enable.'''

    def send_hold(self) -> None:
        '''Transmits hold.'''

    def send_resume(self) -> None:
        '''Transmits resume.'''

    def send_estop(self) -> None:
        '''Transmits estop.'''


class IncompleteControlTransmitterStub:
    '''Incomplete test stub missing required transmitter methods.'''

    def send_enable(self) -> None:
        '''Transmits enable.'''

    def send_hold(self) -> None:
        '''Transmits hold.'''


class IControlTransmitterTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IControlTransmitter.'''

    def test_protocol_conformance_success(self) -> None:
        '''
            Verifies compliant class satisfies IControlTransmitter protocol.

            :exceptions: None.
        '''
        stub = ControlTransmitterStub()
        self.assertIsInstance(stub, IControlTransmitter)

    def test_protocol_conformance_failure(self) -> None:
        '''
            Verifies incomplete class fails IControlTransmitter protocol check.

            :exceptions: None.
        '''
        incomplete = IncompleteControlTransmitterStub()
        self.assertNotIsInstance(incomplete, IControlTransmitter)


if __name__ == '__main__':
    main()
