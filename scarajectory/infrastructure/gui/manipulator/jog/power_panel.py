# -*- coding: UTF-8 -*-

'''
Module
    power_panel.py
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
    Manipulator power and homing control panel subcomponent.
'''

from __future__ import annotations

from tkinter import LEFT, Widget
from tkinter.ttk import Button, Frame
from typing import Final

from scarajectory.core.service.manipulator.imotion_controller import IMotionController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogPowerPanel(Frame):
    '''
        Panel managing manipulator activation, power disable, and homing commands.

        It defines:

            :attributes:
                | _motion_controller - Injected motion controller collaborator.
            :methods:
                | __init__ - Initializes the power and homing buttons.
                | enable - Enables motor drives on the robot manipulator.
                | disable - Disables motor drives on the robot manipulator.
                | home - Commands robot manipulator to execute homing sequence.
    '''

    _motion_controller: IMotionController

    def __init__(
        self,
        parent: Widget,
        *,
        motion_controller: IMotionController,
    ) -> None:
        '''
            Initializes the power and homing buttons layout.

            :param parent: Parent container widget.
            :param motion_controller: Injected IMotionController collaborator.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._motion_controller: Final[IMotionController] = motion_controller

        Button(
            self,
            text='Power ON',
            style='Success.TButton',
            command=self.enable,
        ).pack(side=LEFT, padx=3)

        Button(
            self,
            text='Power OFF',
            style='Danger.TButton',
            command=self.disable,
        ).pack(side=LEFT, padx=3)

        Button(
            self,
            text='Home All',
            command=self.home,
        ).pack(side=LEFT, padx=3)

    def enable(self) -> None:
        '''
            Enables motor drives on the robot manipulator.

            :exceptions: None.
        '''
        self._motion_controller.enable()

    def disable(self) -> None:
        '''
            Disables motor drives on the robot manipulator.

            :exceptions: None.
        '''
        self._motion_controller.disable()

    def home(self) -> None:
        '''
            Commands robot manipulator to execute homing calibration sequence.

            :exceptions: None.
        '''
        self._motion_controller.home()
