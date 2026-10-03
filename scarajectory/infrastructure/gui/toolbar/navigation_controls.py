# -*- coding: UTF-8 -*-

'''
Module
    navigation_controls.py
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
    Viewport navigation and history control buttons for toolbar.
'''

from __future__ import annotations

from tkinter import LEFT, VERTICAL, Widget, Y
from tkinter.ttk import Button, Frame, Separator
from typing import Final

from scarajectory.core.service.trajectory.plan.itrajectory_history import ITrajectoryHistory
from scarajectory.infrastructure.gui.canvas.navigation.icanvas_view_navigator import ICanvasViewNavigator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolbarNavigationControls(Frame):
    '''
        Subcomponent providing viewport zoom, fit, reset, and plan undo/redo.

        It defines:

            :attributes:
                | _navigator - Viewport navigation interface.
                | _history - Trajectory history service interface.
            :methods:
                | __init__ - Initializes navigation controls.
                | build_layout - Builds navigation and history buttons.
                | reset_view - Resets viewport view to 100%.
    '''

    _navigator: ICanvasViewNavigator
    _history: ITrajectoryHistory

    def __init__(
        self,
        parent: Widget,
        navigator: ICanvasViewNavigator,
        history: ITrajectoryHistory,
    ) -> None:
        '''
            Initializes navigation controls.

            :param parent: Parent container widget.
            :param navigator: Viewport navigation interface.
            :param history: Trajectory history service interface.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._navigator: Final[ICanvasViewNavigator] = navigator
        self._history: Final[ITrajectoryHistory] = history
        self.build_layout()

    def build_layout(self) -> None:
        '''
            Builds navigation and history buttons.

            :exceptions: None.
        '''
        Button(
            self, text='[ + ]', width=4, command=self._navigator.zoom_in
        ).pack(side=LEFT, padx=1)
        Button(
            self, text='[ - ]', width=4, command=self._navigator.zoom_out
        ).pack(side=LEFT, padx=1)
        Button(
            self, text='Fit', width=4, command=self._navigator.fit_reach_view
        ).pack(side=LEFT, padx=1)
        Button(
            self, text='100%', width=5, command=self._navigator.reset_view
        ).pack(side=LEFT, padx=1)

        Separator(self, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=8)
        Button(
            self, text='Undo', width=5, command=self._history.undo
        ).pack(side=LEFT, padx=2)
        Button(
            self, text='Redo', width=5, command=self._history.redo
        ).pack(side=LEFT, padx=2)

    def reset_view(self) -> None:
        '''
            Resets viewport view to 100%.

            :exceptions: None.
        '''
        self._navigator.reset_view()
