# -*- coding: UTF-8 -*-

'''
Module
    plan_loader_test.py
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
    Unit tests for PlanLoader file reading and plan deserialization.
'''

from __future__ import annotations

from os import remove
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase, main

from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.options import ConfigIOBundleOptions
from ats_utilities.config_io.storer.engine import Storer
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.storage.config_io.config_io_factory import ConfigIOFactory
from scarajectory.infrastructure.storage.plan_loader import PlanLoader
from scarajectory.infrastructure.storage.trajectory_serializer import TrajectorySerializer

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
        Test cases for PlanLoader file reading and deserialization operations.

        It defines:

            :methods:
                | setUp - Initializes loader test fixture.
                | test_load_plan_missing_file - Tests loading non-existent file returns empty list.
                | test_load_plan_existing_file - Tests loading valid trajectory JSON file.
                | test_load_text_file - Tests reading UTF-8 encoded text file.
                | test_load_binary_file - Tests reading raw bytes from binary file.
    '''

    context_bundle: ContextBundle
    loader: PlanLoader

    def setUp(self) -> None:
        '''
            Sets up test fixture initializing PlanLoader with I/O factory.
        '''
        self.context_bundle = ContextBundleFactory.create_bundle()
        io_factory = ConfigIOFactory.create(self.context_bundle)
        self.loader = PlanLoader(io_factory=io_factory)

    def test_load_plan_missing_file(self) -> None:
        '''
            Verifies load_plan returns an empty list when target file does not exist.
        '''
        waypoints: list[Waypoint] = self.loader.load_plan('/nonexistent/plan/file.json')
        self.assertEqual(waypoints, [])

    def test_load_plan_existing_file(self) -> None:
        '''
            Verifies loading and deserializing waypoints from a valid JSON file.
        '''
        sample_waypoints: list[Waypoint] = [
            Waypoint(x=10.0, y=20.0, z=5.0, phi=0.0, speed=25.0, name='P1', command=''),
            Waypoint(x=30.0, y=40.0, z=15.0, phi=10.0, speed=50.0, name='P2', command='PUMP ON'),
        ]
        payload: dict[str, object] = TrajectorySerializer.serialize_to_dict(sample_waypoints)

        with NamedTemporaryFile(suffix='.json', delete=False) as tf:
            tmp_path: str = tf.name

        try:
            bundle = ConfigIOBundleFactory.create_bundle(
                ConfigIOBundleOptions(
                    file_path=tmp_path,
                    context_bundle=self.context_bundle,
                )
            )
            storer = Storer(bundle)
            storer.store_configuration(payload)

            loaded: list[Waypoint] = self.loader.load_plan(tmp_path)
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded[0].x, 10.0)
            self.assertEqual(loaded[0].name, 'P1')
            self.assertEqual(loaded[1].y, 40.0)
            self.assertEqual(loaded[1].command, 'PUMP ON')
        finally:
            if exists(tmp_path):
                remove(tmp_path)

    def test_load_text_file(self) -> None:
        '''
            Verifies reading UTF-8 encoded text file.
        '''
        content: str = '# SCARA Program\nENABLE\nHOME\n'
        with NamedTemporaryFile(mode='w', suffix='.scara', encoding='utf-8', delete=False) as tf:
            tf.write(content)
            tmp_path: str = tf.name

        try:
            loaded_text: str = self.loader.load_text_file(tmp_path)
            self.assertEqual(loaded_text, content)
        finally:
            if exists(tmp_path):
                remove(tmp_path)

    def test_load_binary_file(self) -> None:
        '''
            Verifies reading raw bytes from a binary file.
        '''
        payload: bytes = b'\xAA\x55\x01\x00\xFF\x0D\x0A'
        with NamedTemporaryFile(mode='wb', suffix='.bin', delete=False) as tf:
            tf.write(payload)
            tmp_path: str = tf.name

        try:
            loaded_bytes: bytes = self.loader.load_binary_file(tmp_path)
            self.assertEqual(loaded_bytes, payload)
        finally:
            if exists(tmp_path):
                remove(tmp_path)


if __name__ == '__main__':
    main()
