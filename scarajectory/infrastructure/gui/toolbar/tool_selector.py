# -*- coding: UTF-8 -*-

'''
Module
    tool_selector.py
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
    CAD drawing tool mode selector subcomponent for toolbar.
'''

from __future__ import annotations

from tkinter import LEFT, StringVar, Widget
from tkinter.ttk import Frame, Label, Radiobutton
from typing import Final

from scarajectory.infrastructure.gui.canvas.icanvas import ICanvas
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolbarToolSelector(Frame):
    '''
        Subcomponent managing CAD mode radiobutton selector controls.

        It defines:

            :attributes:
                | _canvas - Active CAD canvas interface.
                | _tool_var - Active CAD tool mode variable.
            :methods:
                | __init__ - Initializes tool selector controls.
                | build_layout - Builds radiobutton controls for CAD modes.
                | set_tool_mode - Sets current tool mode programmatically.
                | get_tool_mode - Returns current tool mode identifier string.
    '''

    _canvas: ICanvas
    _tool_var: StringVar

    def __init__(
        self,
        parent: Widget,
        canvas: ICanvas,
    ) -> None:
        '''
            Initializes tool selector controls.

            :param parent: Parent container widget.
            :param canvas: Active CAD canvas interface.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._canvas: Final[ICanvas] = canvas
        self._tool_var = StringVar(value='POINT')
        self.build_layout()

    def build_layout(self) -> None:
        '''
            Builds radiobutton controls for CAD modes.

            :exceptions: None.
        '''
        Label(self, text='Tool:', style='Header.TLabel').pack(
            side=LEFT, padx=(0, 4)
        )
        tools: list[tuple[str, str, CanvasToolMode]] = [
            ('Point', 'POINT', CanvasToolMode.POINT),
            ('Line', 'LINE', CanvasToolMode.LINE),
            ('Select/Move', 'SELECT', CanvasToolMode.SELECT),
            ('Circle', 'CIRCLE', CanvasToolMode.CIRCLE),
            ('Rectangle', 'RECTANGLE', CanvasToolMode.RECTANGLE),
            ('Freehand', 'FREEHAND', CanvasToolMode.FREEHAND),
        ]
        for text, val, mode in tools:
            btn = Radiobutton(
                self,
                text=text,
                value=val,
                variable=self._tool_var,
                command=lambda m=mode: self._canvas.set_tool_mode(m),
            )
            btn.pack(side=LEFT, padx=2)

    def set_tool_mode(self, mode: CanvasToolMode) -> None:
        '''
            Sets current tool mode programmatically.

            :param mode: Desired CanvasToolMode.
            :exceptions: None.
        '''
        self._tool_var.set(mode.name)
        self._canvas.set_tool_mode(mode)

    def get_tool_mode(self) -> str:
        '''
            Returns current tool mode identifier string.

            :return: Mode string identifier.
            :exceptions: None.
        '''
        return self._tool_var.get()
