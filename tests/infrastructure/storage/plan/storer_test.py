# -*- coding: UTF-8 -*-

'''
Module
    storer_test.py
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
    Unit tests for PlanStorer component.
'''

from __future__ import annotations

from os import remove
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest.mock import MagicMock

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.plan.store.query.iquery import IWaypointQuery
from scarajectory.infrastructure.storage.config_io.storer.istorer import IConfigStorer
from scarajectory.infrastructure.storage.plan.storer import PlanStorer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlanStorer(TestCase):
    '''
        Test cases verifying PlanStorer operations.

        It defines:

            :methods:
                | setUp - Initializes mock config storer and plan storer.
                | test_save_plan - Verifies saving trajectory plan waypoints.
                | test_save_text_file - Verifies saving text content.
                | test_save_binary_file - Verifies saving binary content.
    '''

    def setUp(self) -> None:
        '''Initializes shared test fixtures.'''
        self.mock_config_storer = MagicMock(spec=IConfigStorer)
        self.storer = PlanStorer(config_storer=self.mock_config_storer)

    def test_save_plan(self) -> None:
        '''Verifies save_plan serializes waypoints and calls config storer.'''
        waypoints = [
            TrajectoryWaypoint(x=10.0, y=20.0, z=30.0, phi=40.0, speed=50.0, name='WP1', command='M1')
        ]
        mock_plan = MagicMock(spec=IWaypointQuery)
        mock_plan.waypoints = waypoints

        with NamedTemporaryFile(suffix='.json', delete=False) as tmp_file:
            tmp_path = tmp_file.name

        try:
            self.storer.save_plan(mock_plan, tmp_path)
            self.mock_config_storer.store.assert_called_once()
        finally:
            if exists(tmp_path):
                remove(tmp_path)

    def test_save_text_file(self) -> None:
        '''Verifies save_text_file writes string content to file.'''
        content = 'hello world text content'
        with NamedTemporaryFile(suffix='.txt', delete=False) as tmp_file:
            tmp_path = tmp_file.name

        try:
            self.storer.save_text_file(content, tmp_path)
            with open(tmp_path, 'r', encoding='utf-8') as f:
                read_content = f.read()
            self.assertEqual(read_content, content)
        finally:
            if exists(tmp_path):
                remove(tmp_path)

    def test_save_binary_file(self) -> None:
        '''Verifies save_binary_file writes binary bytes to file.'''
        content = b'\xDE\xAD\xBE\xEF'
        with NamedTemporaryFile(suffix='.bin', delete=False) as tmp_file:
            tmp_path = tmp_file.name

        try:
            self.storer.save_binary_file(content, tmp_path)
            with open(tmp_path, 'rb') as f:
                read_content = f.read()
            self.assertEqual(read_content, content)
        finally:
            if exists(tmp_path):
                remove(tmp_path)
