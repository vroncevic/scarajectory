# -*- coding: UTF-8 -*-

'''
Module
    streamer_controllers_bundle.py
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
    Parameter bundle holding manipulator controllers for StreamerTab.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.service.manipulator.ijog_controller import IJogController
from scarajectory.core.service.manipulator.imotion_controller import IMotionController
from scarajectory.core.service.tool.itool_controller import IToolController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class StreamerControllersBundle:
    '''
        Bundle containing manipulator controllers for streaming operations.

        It defines:

            :attributes:
                | motion_controller - Motion activation and homing controller.
                | jog_controller - Manual relative axis movement controller.
                | tool_controller - End-effector pneumatic and valve controller.
    '''

    motion_controller: IMotionController
    jog_controller: IJogController
    tool_controller: IToolController
