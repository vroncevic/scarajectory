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
    Unit tests for CommunicationSettingsDependencies dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.settings.communication.dependencies import CommunicationSettingsDependencies
from scarajectory.infrastructure.storage.config_io.loader.iloader import IConfigLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommunicationSettingsDependenciesTestCase(TestCase):
    '''
        Test cases verifying CommunicationSettingsDependencies structure and immutability.

        It defines:

            :methods:
                | test_dependencies_creation - Verifies fields assignment.
                | test_dependencies_immutability - Verifies frozen immutability.
    '''

    def test_dependencies_creation(self) -> None:
        '''
            Verifies CommunicationSettingsDependencies exposes config_loader, config_path, and scheme_path.

            :exceptions: None.
        '''
        mock_loader = MagicMock(spec=IConfigLoader)
        deps = CommunicationSettingsDependencies(
            config_loader=mock_loader,
            config_path='/tmp/comm.json',
            scheme_path='/tmp/comm_scheme.json',
        )
        self.assertIs(deps.config_loader, mock_loader)
        self.assertEqual(deps.config_path, '/tmp/comm.json')
        self.assertEqual(deps.scheme_path, '/tmp/comm_scheme.json')

    def test_dependencies_immutability(self) -> None:
        '''
            Verifies CommunicationSettingsDependencies is frozen and rejects mutation.

            :exceptions: None.
        '''
        deps = CommunicationSettingsDependencies(
            config_loader=MagicMock(spec=IConfigLoader),
            config_path='/tmp/comm.json',
            scheme_path='/tmp/comm_scheme.json',
        )
        with self.assertRaises(FrozenInstanceError):
            deps.config_path = '/tmp/other.json'


if __name__ == '__main__':
    main()
