# -*- coding: UTF-8 -*-

'''
Module
    itoolbar_layout_builder.py
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
    Defines abstract interface for assembling and mounting toolbar layout.
'''

from __future__ import annotations

from tkinter import Tk
from typing import Protocol, runtime_checkable

from scarajectory.infrastructure.gui.canvas.trajectory_canvas import TrajectoryCanvas
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.scarajectory_gui_init_bundle import ScarajectoryGUIInitBundle
from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IToolbarLayoutBuilder(Protocol):
    '''
        Protocol defining contract for constructing and mounting toolbar.

        It defines:

            :methods:
                | build - Constructs and mounts top toolbar in the root window.
                | get_version - Returns interface version string.
    '''

    def build(
        self,
        root: Tk,
        *,
        canvas: TrajectoryCanvas,
        bundle: ScarajectoryGUIInitBundle,
        settings: CanvasSettings,
    ) -> Toolbar:
        '''
            Constructs and mounts top toolbar in the root window.

            :param root: Root Tkinter window.
            :param canvas: TrajectoryCanvas instance.
            :param bundle: GUI initialization dependencies bundle.
            :param settings: Canvas settings configuration.
            :return: Instantiated Toolbar widget.
        '''

    def get_version(self) -> str:
        '''
            Returns the component version string.

            :return: Component version string.
        '''
