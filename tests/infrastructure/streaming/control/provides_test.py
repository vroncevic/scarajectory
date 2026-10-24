# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit testing for ControlProvides dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.streaming.control.itransmitter import IControlTransmitter
from scarajectory.infrastructure.streaming.control.provides import ControlProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestControlProvides(TestCase):
    '''
    Test cases verifying ControlProvides dataclass.

    It defines:

        :methods:
            | test_initialization - Tests attributes and immutability.
    '''

    def test_initialization(self) -> None:
        '''
            Tests dataclass property storage and immutability.

            :exceptions: None.
        '''
        transmitter = MagicMock(spec=IControlTransmitter)
        provides = ControlProvides(control_transmitter=transmitter)
        self.assertIs(provides.control_transmitter, transmitter)


if __name__ == '__main__':
    main()
