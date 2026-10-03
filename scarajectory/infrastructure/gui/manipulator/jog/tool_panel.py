# -*- coding: UTF-8 -*-

'''
Module
    tool_panel.py
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
    Manipulator end-effector tool actuator and pneumatic control subcomponent.
'''

from __future__ import annotations

from tkinter import LEFT, Widget
from tkinter.ttk import Button, Frame
from typing import Final

from scarajectory.core.service.tool.itool_controller import IToolController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogToolPanel(Frame):
    '''
        Panel managing manipulator tooling, vacuum pump and pneumatic valve states.

        It defines:

            :attributes:
                | _tool_controller - Injected end-effector tool controller.
            :methods:
                | __init__ - Initializes pump and valve action buttons.
                | set_pump - Activates or deactivates the vacuum pump.
                | set_valve - Opens or closes the pneumatic purge valve.
    '''

    _tool_controller: IToolController

    def __init__(
        self,
        parent: Widget,
        *,
        tool_controller: IToolController,
    ) -> None:
        '''
            Initializes pump and valve action buttons.

            :param parent: Parent container widget.
            :param tool_controller: Injected IToolController collaborator.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._tool_controller: Final[IToolController] = tool_controller

        Button(
            self,
            text='Pump ON',
            command=lambda: self.set_pump(True),
        ).pack(side=LEFT, padx=2)

        Button(
            self,
            text='Pump OFF',
            command=lambda: self.set_pump(False),
        ).pack(side=LEFT, padx=2)

        Button(
            self,
            text='Valve ON',
            command=lambda: self.set_valve(True),
        ).pack(side=LEFT, padx=2)

        Button(
            self,
            text='Valve OFF',
            command=lambda: self.set_valve(False),
        ).pack(side=LEFT, padx=2)

    def set_pump(self, state: bool) -> None:
        '''
            Activates or deactivates the vacuum pump.

            :param state: True to activate, False to deactivate.
            :exceptions: None.
        '''
        self._tool_controller.set_vacuum_pump(state)

    def set_valve(self, state: bool) -> None:
        '''
            Opens or closes the pneumatic purge valve.

            :param state: True to open, False to close.
            :exceptions: None.
        '''
        self._tool_controller.set_valve(state)
