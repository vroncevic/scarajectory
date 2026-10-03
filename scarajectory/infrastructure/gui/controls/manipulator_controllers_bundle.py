# -*- coding: UTF-8 -*-

'''
Module
    manipulator_controllers_bundle.py
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
    Immutable value bundle holding assembled manipulator sub-controllers.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.infrastructure.manipulator.jog_controller import JogController
from scarajectory.infrastructure.manipulator.motion_controller import MotionController
from scarajectory.infrastructure.manipulator.query_controller import QueryController
from scarajectory.infrastructure.tool.tool_controller import ToolController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class ManipulatorControllersBundle:
    '''
        Bundle containing assembled manipulator sub-controllers.

        It defines:

            :attributes:
                | motion_ctrl - MotionController managing arm power and home.
                | jog_ctrl - JogController managing manual axis jog motions.
                | tool_ctrl - ToolController managing toolhead actuators.
                | query_ctrl - QueryController managing hardware status.
    '''

    motion_ctrl: MotionController
    jog_ctrl: JogController
    tool_ctrl: ToolController
    query_ctrl: QueryController
