# -*- coding: UTF-8 -*-

'''
Module
    plan_storer_test.py
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
    Unit tests for PlanStorer file writing and plan serialization.
'''

from __future__ import annotations

from os import remove
from os.path import exists, join
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest import TestCase, main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory
from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.plan.store.waypoint_store_factory import (
    WaypointStoreFactory,
)
from scarajectory.infrastructure.storage.plan_loader import PlanLoader
from scarajectory.infrastructure.storage.plan_storer import PlanStorer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlanStorer(TestCase):
    '''
        Test cases for PlanStorer serialization and file writing operations.

        It defines:

            :methods:
                | setUp - Initializes storer test fixture.
                | test_save_plan - Tests saving trajectory plan to JSON file and reading back.
                | test_save_text_file - Tests writing text file with parent directory creation.
                | test_save_binary_program - Tests writing BinaryProgram raw bytes to file.
    '''

    context_bundle: ContextBundle
    storer: PlanStorer
    loader: PlanLoader

    def setUp(self) -> None:
        '''
            Sets up test fixture initializing PlanStorer and PlanLoader.
        '''
        self.context_bundle = ContextBundleFactory.create_bundle()
        self.storer = PlanStorer(context_bundle=self.context_bundle)
        self.loader = PlanLoader(context_bundle=self.context_bundle)

    def test_save_plan(self) -> None:
        '''
            Verifies saving trajectory plan waypoints to JSON file via ATS Storer.
        '''
        waypoints: list[Waypoint] = [
            Waypoint(x=15.0, y=25.0, z=10.0, phi=5.0, speed=40.0, name='W1', command=''),
            Waypoint(x=35.0, y=45.0, z=20.0, phi=15.0, speed=60.0, name='W2', command='VALVE 1'),
        ]
        plan = WaypointStoreFactory.create_with_waypoints(waypoints)

        with NamedTemporaryFile(suffix='.json', delete=False) as tf:
            tmp_path: str = tf.name

        try:
            self.storer.save_plan(plan, tmp_path)
            self.assertTrue(exists(tmp_path))

            loaded: list[Waypoint] = self.loader.load_plan(tmp_path)
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded[0].x, 15.0)
            self.assertEqual(loaded[0].name, 'W1')
            self.assertEqual(loaded[1].command, 'VALVE 1')
        finally:
            if exists(tmp_path):
                remove(tmp_path)

    def test_save_text_file(self) -> None:
        '''
            Verifies writing text file with automatic parent directory creation.
        '''
        with TemporaryDirectory() as tmp_dir:
            nested_path: str = join(tmp_dir, 'subfolder', 'program.scara')
            content: str = '# Test program\nENABLE\nMOVE_J X=100.0 Y=50.0\n'

            self.storer.save_text_file(content, nested_path)
            self.assertTrue(exists(nested_path))

            read_back: str = self.loader.load_text_file(nested_path)
            self.assertEqual(read_back, content)

    def test_save_binary_program(self) -> None:
        '''
            Verifies saving compiled BinaryProgram raw bytes to destination file.
        '''
        raw_bytes = b'\xAA\x55\x01\x02\x03\x04\x0D\x0A'
        telemetry = BinaryProgramTelemetry(
            source_instructions=1,
            compiled_steps=0,
            duration_us=1000,
            duration_s=0.001,
            peak_j1_steps=0,
            peak_j2_steps=0,
            peak_z_steps=0,
            peak_j4_steps=0,
            total_wire_bytes=8,
        )
        program = BinaryProgram(
            steps=(),
            raw_bytes=raw_bytes,
            total_duration_us=1000,
            instruction_count=1,
            step_counts=(0, 0, 0, 0),
            telemetry=telemetry,
        )

        with TemporaryDirectory() as tmp_dir:
            nested_path: str = join(tmp_dir, 'bin_sub', 'program.bin')

            self.storer.save_binary_program(program, nested_path)
            self.assertTrue(exists(nested_path))

            read_bytes: bytes = self.loader.load_binary_file(nested_path)
            self.assertEqual(read_bytes, program.raw_bytes)


if __name__ == '__main__':
    main()
