# -*- coding: UTF-8 -*-

'''
Module
    plan_storage_service_test.py
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
    Unit tests for PlanStorageService persistence using ats_utilities.
'''

from __future__ import annotations

from os import remove
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.plan.store.waypoint_store_factory import WaypointStoreFactory
from scarajectory.infrastructure.storage.plan_storage_service_factory import PlanStorageServiceFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlanStorageService(TestCase):
    '''
        Test cases for PlanStorageService persistence operations.

        It defines:

            :methods:
                | test_save_and_load_plan - Tests writing and reading trajectory JSON file via ATS Storer/Loader.
                | test_load_plan_missing_file - Tests loading non-existent file returns empty list.
                | test_save_and_load_text_file - Tests writing and reading UTF-8 text file.
                | test_save_and_load_binary_file - Tests writing and reading binary program file.
    '''

    def test_save_and_load_plan(self) -> None:
        '''
            Tests roundtrip file storage and retrieval using ATS Storer and Loader.
        '''
        storage = PlanStorageServiceFactory.create()
        plan = WaypointStoreFactory.create_with_waypoints([
            Waypoint(x=50.0, y=60.0, z=20.0, phi=0.0, speed=30.0, name='P1', command=''),
            Waypoint(x=70.0, y=80.0, z=20.0, phi=0.0, speed=30.0, name='P2', command=''),
        ])

        with NamedTemporaryFile(suffix='.json', delete=False) as tf:
            tmp_path = tf.name

        try:
            storage.save_plan(plan, tmp_path)
            loaded_pts = storage.load_plan(tmp_path)
            self.assertEqual(len(loaded_pts), 2)
            self.assertEqual(loaded_pts[0].x, 50.0)
            self.assertEqual(loaded_pts[1].x, 70.0)
            self.assertEqual(loaded_pts[0].name, 'P1')
            self.assertEqual(loaded_pts[1].name, 'P2')
        finally:
            if exists(tmp_path):
                remove(tmp_path)

    def test_load_plan_missing_file(self) -> None:
        '''
            Tests loading a non-existent file path returns an empty list.
        '''
        storage = PlanStorageServiceFactory.create()
        result = storage.load_plan('/tmp/non_existent_trajectory_file_12345.json')
        self.assertEqual(result, [])

    def test_save_and_load_text_file(self) -> None:
        '''
            Tests writing and reading text content with UTF-8 encoding.
        '''
        storage = PlanStorageServiceFactory.create()
        content = 'G00 X100 Y50 Z20\nPOINT X=20 Y=30 Z=10\n'
        with NamedTemporaryFile(suffix='.scara', delete=False) as tf:
            tmp_path = tf.name

        try:
            storage.save_text_file(content, tmp_path)
            read_back = storage.load_text_file(tmp_path)
            self.assertEqual(read_back, content)
        finally:
            if exists(tmp_path):
                remove(tmp_path)

    def test_save_and_load_binary_file(self) -> None:
        '''
            Tests writing and reading binary data.
        '''
        storage = PlanStorageServiceFactory.create()
        raw_bytes = b'\x01\x02\x03\x04\x05'
        with NamedTemporaryFile(suffix='.bin', delete=False) as tf:
            tmp_path = tf.name

        try:
            storage.save_binary_file(raw_bytes, tmp_path)
            read_back = storage.load_binary_file(tmp_path)
            self.assertEqual(read_back, raw_bytes)
        finally:
            if exists(tmp_path):
                remove(tmp_path)


if __name__ == '__main__':
    main()
