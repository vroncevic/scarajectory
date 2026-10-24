# -*- coding: UTF-8 -*-

'''
Module
    loader_test.py
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
    Unit tests for PlanLoader component.
'''

from __future__ import annotations

from os import remove
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest.mock import MagicMock

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.storage.config_io.loader.iloader import IConfigLoader
from scarajectory.infrastructure.storage.plan.loader import PlanLoader
from scarajectory.infrastructure.storage.serializer.serializer import TrajectorySerializer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlanLoader(TestCase):
    '''
        Test cases verifying PlanLoader operations.

        It defines:

            :methods:
                | setUp - Initializes mock loader and plan loader.
                | test_load_plan_missing_file - Tests load_plan with non-existent file path.
                | test_load_plan_success - Tests load_plan with mock configuration loader.
                | test_load_text_file - Tests loading text file content.
                | test_load_binary_file - Tests loading raw binary file bytes.
    '''

    def setUp(self) -> None:
        '''Initializes shared test fixtures.'''
        self.mock_config_loader = MagicMock(spec=IConfigLoader)
        self.loader = PlanLoader(config_loader=self.mock_config_loader)

    def test_load_plan_missing_file(self) -> None:
        '''Verifies load_plan returns empty list when file does not exist.'''
        self.assertEqual(self.loader.load_plan('/nonexistent/file.json'), [])

    def test_load_plan_success(self) -> None:
        '''Verifies load_plan loads and deserializes waypoints using config loader.'''
        expected_waypoints = [
            TrajectoryWaypoint(x=10.0, y=20.0, z=30.0, phi=40.0, speed=50.0, name='WP1', command='M1')
        ]
        serialized_data = TrajectorySerializer.serialize_to_dict(expected_waypoints)
        self.mock_config_loader.load.return_value = serialized_data

        with NamedTemporaryFile(suffix='.json', delete=False) as tmp_file:
            tmp_path = tmp_file.name

        try:
            loaded_waypoints = self.loader.load_plan(tmp_path)
            self.assertEqual(len(loaded_waypoints), 1)
            self.assertEqual(loaded_waypoints[0].name, 'WP1')
            self.mock_config_loader.load.assert_called_once_with(tmp_path)
        finally:
            if exists(tmp_path):
                remove(tmp_path)

    def test_load_text_file(self) -> None:
        '''Verifies load_text_file reads file content using UTF-8 encoding.'''
        content = 'line 1\nline 2\nline 3'
        with NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp_file:
            tmp_file.write(content)
            tmp_path = tmp_file.name

        try:
            result = self.loader.load_text_file(tmp_path)
            self.assertEqual(result, content)
        finally:
            if exists(tmp_path):
                remove(tmp_path)

    def test_load_binary_file(self) -> None:
        '''Verifies load_binary_file reads binary file content.'''
        content = b'\x00\x01\x02\x03\xFF'
        with NamedTemporaryFile(mode='wb', suffix='.bin', delete=False) as tmp_file:
            tmp_file.write(content)
            tmp_path = tmp_file.name

        try:
            result = self.loader.load_binary_file(tmp_path)
            self.assertEqual(result, content)
        finally:
            if exists(tmp_path):
                remove(tmp_path)
