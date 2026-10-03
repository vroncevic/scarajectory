# -*- coding: UTF-8 -*-

'''
Module
    waypoint_edit_applier_factory_test.py
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
    Unit testing for WaypointEditApplierFactory component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.editor.waypoint_edit_applier import (
    WaypointEditApplier,
)
from scarajectory.infrastructure.gui.editor.waypoint_edit_applier_factory import (
    WaypointEditApplierFactory,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointEditApplierFactoryTestCase(TestCase):
    '''
        Unit tests for WaypointEditApplierFactory.

        It defines:

            :methods:
                | test_create - Verifies factory returns WaypointEditApplier instance.
                | test_get_version - Verifies factory exposes semantic version string.
    '''

    def test_create(self) -> None:
        '''Verifies factory instantiates a valid WaypointEditApplier object.'''
        applier = WaypointEditApplierFactory.create()
        self.assertIsInstance(applier, WaypointEditApplier)

    def test_get_version(self) -> None:
        '''Verifies factory provides semantic version string matching package.'''
        self.assertEqual(WaypointEditApplierFactory.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
