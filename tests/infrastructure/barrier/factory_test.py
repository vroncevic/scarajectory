# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for BarrierFactory component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaracom.flow.barrier.ibarrier import IFlowBarrier

from scarajectory.infrastructure.barrier.factory import BarrierFactory
from scarajectory.infrastructure.barrier.provides import BarrierProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBarrierFactory(TestCase):
    '''
        Test cases for BarrierFactory component.

        It defines:

            :methods:
                | test_barrier_factory_create - Verifies BarrierFactory constructs BarrierProvides.
                | test_barrier_factory_version - Verifies get_version returns semantic version string.
    '''

    def test_barrier_factory_create(self) -> None:
        '''
            Verifies factory construction returning BarrierProvides with IFlowBarrier.

            :exceptions: None.
        '''
        provides = BarrierFactory.create()
        self.assertIsInstance(provides, BarrierProvides)
        self.assertIsInstance(provides.flow_barrier, IFlowBarrier)

    def test_barrier_factory_version(self) -> None:
        '''
            Verifies factory version string retrieval.

            :exceptions: None.
        '''
        version = BarrierFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.0.3')


if __name__ == '__main__':
    main()
