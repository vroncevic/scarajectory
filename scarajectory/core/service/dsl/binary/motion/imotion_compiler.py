# -*- coding: UTF-8 -*-

'''
Module
    imotion_compiler.py
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
    Defines IMotionCompiler Protocol for compiling motion waypoints into binary steps.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.dsl.binary.step import Step
from scarajectory.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMotionCompiler(Protocol):
    '''
        Structural protocol defining contracts for compiling motion waypoints into binary steps.

        It defines:

            :methods:
                | compile_motion_step - Compiles a motion waypoint into a binary joint move step.
    '''

    def compile_motion_step(
        self,
        *,
        waypoint: Waypoint,
        seq_num: int,
        prev_angles: tuple[float, float, float, float] | None,
        line_num: int
    ) -> tuple[Step, tuple[float, float, float, float]]:
        '''
            Compiles a motion waypoint into a binary joint move step.

            :param waypoint: Target Cartesian waypoint.
            :param seq_num: Frame sequence counter.
            :param prev_angles: Previous joint angles tuple or None.
            :param line_num: Source line index.
            :return: Tuple of compiled Step and updated joint angles tuple.
        '''
