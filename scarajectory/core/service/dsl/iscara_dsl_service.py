# -*- coding: UTF-8 -*-

'''
Module
    iscara_dsl_service.py
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
    Defines interface IScaraDslService coordinating high-level SCARA DSL compilation and export.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.dsl.scara_diagnostic import ScaraDiagnostic
from scarajectory.core.model.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.model.scara_bounds import ScaraBounds
from scarajectory.core.model.trajectory_plan import TrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraDslService(Protocol):
    '''
        High-level orchestration service for SCARA DSL source processing.

        It defines:

            :methods:
                | compile_script - Compiles DSL source code into executable TrajectoryPlan.
                | validate_script - Checks syntax and kinematics of DSL script.
                | lint_script - Performs static analysis checks on DSL script string.
                | export_plan - Serializes active TrajectoryPlan to DSL source text.
    '''

    def compile_script(
        self,
        *,
        source: str,
        bounds: ScaraBounds | None = None,
    ) -> TrajectoryPlan:
        '''
            Compiles DSL source code into an executable and validated TrajectoryPlan.

            :param source: Raw .scara script text.
            :param bounds: Optional robot kinematic boundary constraints.
            :return: Validated TrajectoryPlan instance.
            :exceptions: ValueError if parsing or kinematic validation fails.
        '''

    def validate_script(
        self,
        *,
        source: str,
        bounds: ScaraBounds | None = None,
    ) -> tuple[bool, list[str]]:
        '''
            Validates syntax and kinematic feasibility of a DSL script without mutating active plan.

            :param source: Raw .scara script text.
            :param bounds: Optional robot kinematic boundary constraints.
            :return: Tuple of (is_valid, messages_list).
            :exceptions: None.
        '''

    def lint_script(
        self,
        *,
        source: str,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Performs static analysis checks on a DSL script string.

            :param source: Raw .scara script text.
            :return: Tuple of ScaraDiagnostic findings.
            :exceptions: None.
        '''

    def export_plan(self, *, plan: ITrajectoryPlan) -> str:
        '''
            Serializes active TrajectoryPlan into formatted .scara DSL source text.

            :param plan: TrajectoryPlan instance to serialize.
            :return: Formatted SCARA DSL script.
            :exceptions: None.
        '''
