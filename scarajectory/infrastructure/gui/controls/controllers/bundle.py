# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Immutable value bundle holding assembled hardware sub-controllers for tabs.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.service.manipulator.ijog import IJogController
from scarajectory.core.service.manipulator.imotion import IMotionController
from scarajectory.core.service.manipulator.iquery import IQueryController
from scarajectory.core.service.tool.icontroller import IToolController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class TabControllersBundle:
    '''
        Bundle containing assembled hardware sub-controllers for control tabs.

        It defines:

            :attributes:
                | motion_ctrl - IMotionController managing arm power and home.
                | jog_ctrl - IJogController managing manual axis jog motions.
                | tool_ctrl - IToolController managing toolhead actuators.
                | query_ctrl - IQueryController managing hardware status.
    '''

    motion_ctrl: IMotionController
    jog_ctrl: IJogController
    tool_ctrl: IToolController
    query_ctrl: IQueryController
