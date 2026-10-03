# -*- coding: UTF-8 -*-

'''
Module
    canvas_event_context.py
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
    Immutable context holding canvas geometry and configuration for mouse events.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True)
class CanvasEventContext:
    '''
        Immutable container holding viewport dimensions and active canvas settings.

        It defines:

            :attributes:
                | width - Current canvas viewport width in pixels.
                | height - Current canvas viewport height in pixels.
                | tool_mode - Active drawing or selection tool mode.
                | settings - Active canvas parameters and deadzone configuration.
    '''

    width: int
    height: int
    tool_mode: CanvasToolMode
    settings: CanvasSettings
