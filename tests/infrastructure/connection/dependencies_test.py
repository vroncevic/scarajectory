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
    Unit testing for ConnectionDependencies bundle.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.connection.dependencies import ConnectionDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionDependenciesTestCase(TestCase):
    '''
        Test cases for ConnectionDependencies parameter bundle.
    '''

    def test_bundle_attributes(self) -> None:
        '''
            Verifies bundle stores all injected parameters.

            :exceptions: None.
        '''
        mock_transport = MagicMock()
        mock_packer = MagicMock()
        mock_listener = MagicMock()
        deps = ConnectionDependencies(
            transport=mock_transport,
            frame_packer=mock_packer,
            listener=mock_listener,
        )
        self.assertIs(deps.transport, mock_transport)
        self.assertIs(deps.frame_packer, mock_packer)
        self.assertIs(deps.listener, mock_listener)

    def test_bundle_frozen(self) -> None:
        '''
            Verifies bundle is frozen and immutable.

            :exceptions: None.
        '''
        deps = ConnectionDependencies(
            transport=MagicMock(),
            frame_packer=MagicMock(),
            listener=MagicMock(),
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(deps, 'transport', MagicMock())


if __name__ == '__main__':
    main()
