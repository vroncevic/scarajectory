# -*- coding: UTF-8 -*-

'''
Module
    fault_event_factory_test.py
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
    Unit tests for FaultEventFactory fault event model factory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.telemetry.fault_event import FaultEvent
from scarajectory.core.service.telemetry.fault_event_factory import (
    FaultEventFactory,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FaultEventFactoryTestCase(TestCase):
    '''
        Tests for FaultEventFactory component.

        It defines:

            :methods:
                | test_create_fault_event - Verifies fault event model creation.
                | test_get_version - Verifies factory version accessor string.
    '''

    def test_create_fault_event(self) -> None:
        '''
            Verifies fault event model creation.

            :exceptions: None.
        '''
        event = FaultEventFactory.create(
            severity=2,
            fault_code=105,
            extra_info=4,
        )
        self.assertIsInstance(event, FaultEvent)
        self.assertEqual(event.severity, 2)
        self.assertEqual(event.fault_code, 105)
        self.assertEqual(event.extra_info, 4)

    def test_get_version(self) -> None:
        '''
            Verifies factory version accessor string.

            :exceptions: None.
        '''
        self.assertEqual(FaultEventFactory.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
