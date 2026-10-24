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
    Unit tests for BarrierProvides container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scaracom.flow.barrier.ibarrier import IFlowBarrier
from scarajectory.infrastructure.barrier.provides import BarrierProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBarrierProvides(TestCase):
    '''
        Unit tests validating BarrierProvides data container.

        It defines:

            :methods:
                | test_barrier_provides_attributes - Verifies BarrierProvides holds expected flow_barrier.
                | test_barrier_provides_frozen - Verifies BarrierProvides is immutable.
    '''

    def test_barrier_provides_attributes(self) -> None:
        '''
            Verifies BarrierProvides holds expected flow_barrier attribute.

            :exceptions: None.
        '''
        mock_barrier = MagicMock(spec=IFlowBarrier)
        provides = BarrierProvides(flow_barrier=mock_barrier)
        self.assertIs(provides.flow_barrier, mock_barrier)

    def test_barrier_provides_frozen(self) -> None:
        '''
            Verifies BarrierProvides is immutable (frozen).

            :exceptions: None.
        '''
        mock_barrier = MagicMock(spec=IFlowBarrier)
        provides = BarrierProvides(flow_barrier=mock_barrier)
        with self.assertRaises(FrozenInstanceError):
            provides.flow_barrier = MagicMock(spec=IFlowBarrier)  # type: ignore[misc]


if __name__ == '__main__':
    main()
