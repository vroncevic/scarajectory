# -*- coding: UTF-8 -*-

'''
Module
    motion_compiler.py
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
    Compiles Cartesian motion waypoints into discrete joint steps and binary move frames.
'''

from __future__ import annotations

from scarajectory.core.model.communication.protocol.binary_frame import BinaryFrame
from scarajectory.core.model.dsl.binary.step import Step
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.communication.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.core.service.dsl.binary.step.istep_discretizer import IStepDiscretizer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionCompiler:
    '''
        Compiles Cartesian motion waypoints into discrete joint steps and binary move frames.

        It defines:

            :attributes:
                | _discretizer - Kinematic discretization service.
                | _frame_builder - Binary frame assembler protocol.
            :methods:
                | __init__ - Initializes motion step compiler with injected collaborators.
                | compile_motion_step - Compiles a single motion waypoint into a binary step.
    '''

    _discretizer: IStepDiscretizer
    _frame_builder: IBinaryFrameBuilder

    def __init__(self, *, discretizer: IStepDiscretizer, frame_builder: IBinaryFrameBuilder) -> None:
        '''
            Initializes motion step compiler with injected collaborators.

            :param discretizer: Injected IStepDiscretizer protocol.
            :param frame_builder: Injected IBinaryFrameBuilder protocol.
            :exceptions: None.
        '''
        self._discretizer = discretizer
        self._frame_builder = frame_builder

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
            :exceptions: ValueError if kinematic solving fails.
        '''
        joint_steps, new_angles = self._discretizer.discretize_waypoint(
            waypoint=waypoint, prev_angles=prev_angles
        )
        frame: BinaryFrame = self._frame_builder.build_joint_move(
            seq_num=seq_num, steps=joint_steps
        )
        raw_bytes: bytes = self._frame_builder.pack_frame(frame=frame)
        target_steps = (
            joint_steps.target_j1_steps,
            joint_steps.target_j2_steps,
            joint_steps.target_z_steps,
            joint_steps.target_j4_steps
        )
        step = Step(
            frame=frame,
            raw_bytes=raw_bytes,
            duration_us=joint_steps.duration_us,
            target_steps=target_steps,
            description=f'MOVE X={waypoint.x:.1f} Y={waypoint.y:.1f} Z={waypoint.z:.1f}',
            line_number=line_num
        )

        return step, new_angles
