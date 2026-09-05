# -*- coding: UTF-8 -*-

'''
Module
    scara_dsl_service_test.py
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
    Unit tests for ScaraDslService compilation, validation and plan export.
'''

from __future__ import annotations

from pathlib import Path
from sys import path
from unittest import TestCase

pkg_dir = str(Path(__file__).resolve().parent.parent)
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.trajectory_plan import TrajectoryPlan
from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.service.dsl.scara_dsl_service import ScaraDslService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraDslService(TestCase):
    '''
        Test cases verifying ScaraDslService facade operations.

        It defines:

            :methods:
                | test_compile_script_success - Verifies compiling valid SCARA script.
                | test_validate_script - Verifies script validation returning diagnostics.
                | test_export_plan - Verifies round-trip plan export to SCARA DSL code.
                | test_compile_pick_and_place_with_tool_and_wait - Verifies pick and place compilation.
                | test_lint_script - Verifies diagnostic reporting through lint_script facade.
    '''

    def test_compile_script_success(self) -> None:
        '''
            Verifies compiling valid SCARA script into populated TrajectoryPlan.
        '''
        service = ScaraDslService()
        code = (
            'CONFIG ELBOW RIGHT\n'
            'SPEED RAPID 100.0\n'
            'MOVE_J X=150.0 Y=50.0 Z=20.0\n'
            'MOVE_L X=160.0 Y=60.0 Z=20.0 SPEED=40.0\n'
        )
        plan = service.compile_script(source=code)
        self.assertGreaterEqual(plan.count, 2)
        first_pt = plan.waypoints[0]
        self.assertAlmostEqual(first_pt.x, 150.0)
        self.assertAlmostEqual(first_pt.y, 50.0)

    def test_validate_script(self) -> None:
        '''
            Verifies validation diagnostics for valid and invalid scripts.
        '''
        service = ScaraDslService()
        valid_code = 'MOVE_J X=150.0 Y=50.0 Z=20.0\n'
        is_valid, msgs = service.validate_script(source=valid_code)
        self.assertTrue(is_valid)
        self.assertTrue(any('PASSED' in m for m in msgs))

        # Test script exceeding reach
        invalid_code = 'MOVE_J X=9999.0 Y=9999.0 Z=20.0\n'
        is_valid_inv, msgs_inv = service.validate_script(source=invalid_code)
        self.assertFalse(is_valid_inv)
        self.assertTrue(len(msgs_inv) > 0)

    def test_export_plan(self) -> None:
        '''
            Verifies exporting a TrajectoryPlan into SCARA DSL source text.
        '''
        service = ScaraDslService()
        plan = TrajectoryPlan()
        plan.add_point(Waypoint(x=150.0, y=50.0, z=10.0, phi=0.0, speed=30.0, name='P1'))
        plan.add_point(Waypoint(x=180.0, y=60.0, z=10.0, phi=15.0, speed=40.0, name='P2'))

        exported = service.export_plan(plan=plan)
        self.assertIn('MOVE_J X=150.00 Y=50.00', exported)
        self.assertIn('MOVE_L X=180.00 Y=60.00', exported)
        self.assertIn('# P1', exported)
        self.assertIn('# P2', exported)

    def test_compile_pick_and_place_with_tool_and_wait(self) -> None:
        '''
            Verifies compiling a pick and place script containing tool and wait instructions.
        '''
        service = ScaraDslService()
        code = (
            'MOVE_J X=150.0 Y=50.0 Z=20.0\n'
            'WAIT 200\n'
            'PUMP ON\n'
            'MOVE_L X=160.0 Y=60.0 Z=10.0\n'
            'PUMP OFF\n'
            'VALVE ON\n'
            'WAIT 100\n'
            'VALVE OFF\n'
        )
        plan = service.compile_script(source=code)
        commands = [pt.command for pt in plan.waypoints if pt.command]
        self.assertIn('<CMD:WAIT#200>', commands)
        self.assertIn('<CMD:PUMP#1>', commands)
        self.assertIn('<CMD:PUMP#0>', commands)
        self.assertIn('<CMD:VALVE#1>', commands)
        self.assertIn('<CMD:VALVE#0>', commands)
        self.assertIn('<CMD:WAIT#100>', commands)

    def test_lint_script(self) -> None:
        '''
            Verifies diagnostic reporting through lint_script facade.
        '''
        service = ScaraDslService()
        code = (
            'HOME\n'
            'PUMP ON\n'
            'PUMP ON\n'
        )
        diagnostics = service.lint_script(source=code)
        self.assertTrue(any(d.code == 'REDUNDANT_TOOL_CMD' for d in diagnostics))

    def test_compile_enable_and_disable(self) -> None:
        '''
            Verifies compiling ENABLE and DISABLE commands into action waypoints.
        '''
        service = ScaraDslService()
        code = (
            'ENABLE\n'
            'HOME\n'
            'DISABLE\n'
        )
        plan = service.compile_script(source=code)
        commands = [pt.command for pt in plan.waypoints if pt.command]
        self.assertIn('<CMD:ENABLE>', commands)
        self.assertIn('<CMD:HOME>', commands)
        self.assertIn('<CMD:DISABLE>', commands)

