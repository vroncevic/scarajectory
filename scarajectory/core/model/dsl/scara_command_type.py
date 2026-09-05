# -*- coding: UTF-8 -*-

'''
Module
    scara_command_type.py
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
    Defines ScaraCommandType enumeration representing all supported SCARA DSL command types.
'''

from __future__ import annotations

from enum import Enum, unique

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@unique
class ScaraCommandType(Enum):
    '''
        Enumeration of supported SCARA Domain-Specific Language (DSL) command types.

        It defines:

            :attributes:
                | CONFIG_ELBOW - Kinematic elbow arm configuration (LEFT or RIGHT).
                | SPEED - Feedrate speed setting (RAPID or WORK).
                | ACCEL - Path acceleration setting.
                | OVERRIDE - Real-time global speed override percentage.
                | HOME - Multi-axis homing sequence.
                | MOVE_J - Fast point-to-point joint move.
                | MOVE_L - Linear Cartesian interpolated motion.
                | JUMP - 3D parabolic arch pick-and-place motion.
                | ARC_CW - Circular arc clockwise.
                | ARC_CCW - Circular arc counter-clockwise.
                | SPLINE - Smooth spline / Bézier curve interpolation.
                | APPROACH - Relative vertical approach along Z.
                | RETRACT - Relative vertical retract along Z.
                | JOG_AXIS - Relative manual jog along Cartesian axis.
                | JOG_JOINT - Relative manual rotation of joint.
                | ZONE - Corner path blending mode (FINE or BLEND).
                | TOOL_ORIENT - End-effector 4th axis orientation mode.
                | FRAME_SET - Definition of local work coordinate frame.
                | FRAME_RESET - Reset coordinates to base world frame.
                | PALLET_DEF - Matrix pallet definition.
                | MOVE_PALLET - Move to index in defined pallet.
                | PROBE - Tactile contact search until trigger.
                | TOOL - End-effector vertical actuation (UP or DOWN).
                | PUMP - Vacuum pump actuation (ON or OFF).
                | VALVE - Release valve actuation (ON or OFF).
                | WAIT_MS - Time delay in milliseconds.
                | SYNC - Wait for motion queue buffer to complete.
                | HOLD - Feed hold / pause trajectory.
                | RESUME - Resume paused trajectory.
                | ESTOP - Immediate emergency stop.
                | ENABLE - Energize robot stepper driver stages.
                | DISABLE - De-energize robot stepper driver stages.
            :methods:
                | None.
    '''

    CONFIG_ELBOW = 'CONFIG_ELBOW'
    SPEED = 'SPEED'
    ACCEL = 'ACCEL'
    OVERRIDE = 'OVERRIDE'
    HOME = 'HOME'
    MOVE_J = 'MOVE_J'
    MOVE_L = 'MOVE_L'
    JUMP = 'JUMP'
    ARC_CW = 'ARC_CW'
    ARC_CCW = 'ARC_CCW'
    SPLINE = 'SPLINE'
    APPROACH = 'APPROACH'
    RETRACT = 'RETRACT'
    JOG_AXIS = 'JOG_AXIS'
    JOG_JOINT = 'JOG_JOINT'
    ZONE = 'ZONE'
    TOOL_ORIENT = 'TOOL_ORIENT'
    FRAME_SET = 'FRAME_SET'
    FRAME_RESET = 'FRAME_RESET'
    PALLET_DEF = 'PALLET_DEF'
    MOVE_PALLET = 'MOVE_PALLET'
    PROBE = 'PROBE'
    TOOL = 'TOOL'
    PUMP = 'PUMP'
    VALVE = 'VALVE'
    WAIT_MS = 'WAIT_MS'
    SYNC = 'SYNC'
    HOLD = 'HOLD'
    RESUME = 'RESUME'
    ESTOP = 'ESTOP'
    ENABLE = 'ENABLE'
    DISABLE = 'DISABLE'
