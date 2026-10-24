# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit testing for ManagerDependencies bundle.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.connection.manager.dependencies import ManagerDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ManagerDependenciesTestCase(TestCase):
    '''
        Test cases for ManagerDependencies parameter bundle.
    '''

    def test_bundle_attributes(self) -> None:
        '''
            Verifies bundle stores connection coordinator.

            :exceptions: None.
        '''
        mock_conn = MagicMock()
        deps = ManagerDependencies(connection_coordinator=mock_conn)
        self.assertIs(deps.connection_coordinator, mock_conn)

    def test_bundle_frozen(self) -> None:
        '''
            Verifies bundle is frozen and immutable.

            :exceptions: None.
        '''
        mock_conn = MagicMock()
        deps = ManagerDependencies(connection_coordinator=mock_conn)
        with self.assertRaises(FrozenInstanceError):
            setattr(deps, 'connection_coordinator', MagicMock())


if __name__ == '__main__':
    main()
