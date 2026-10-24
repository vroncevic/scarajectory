# -*- coding: UTF-8 -*-

'''
Module
    actuator.py
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
    Manipulator homing, vacuum pump and purge valve control actuator section.
'''

from __future__ import annotations

from tkinter import LEFT, Widget
from tkinter.ttk import Button, Frame
from typing import Final

from scarajectory.infrastructure.gui.manipulator.override.idelegate import IManipulatorActionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ActuatorSection(Frame):
    '''
        Section providing robot homing, vacuum pump and purge valve controls.

        It defines:

            :attributes:
                | _action_delegate - Action delegate handling manipulator actuation commands.
                | _btn_pump - Toggle button widget for vacuum pump control.
            :methods:
                | __init__ - Initializes actuator action buttons layout.
                | on_home_robot - Handles click event on home robot button.
                | on_toggle_pump - Handles click event on toggle pump button.
                | on_purge_valve - Handles click event on purge valve button.
                | set_pump_active - Updates pump button text according to active state.
    '''

    _action_delegate: IManipulatorActionDelegate
    _btn_pump: Button

    def __init__(
        self,
        parent: Widget,
        *,
        action_delegate: IManipulatorActionDelegate,
    ) -> None:
        '''
            Initializes actuator action buttons layout.

            :param parent: Parent container widget.
            :param action_delegate: Injected action delegate collaborator.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._action_delegate: Final[IManipulatorActionDelegate] = action_delegate

        Button(
            self,
            text='Home Robot',
            command=self.on_home_robot,
        ).pack(side=LEFT, padx=3)

        self._btn_pump = Button(
            self,
            text='Pump: OFF',
            command=self.on_toggle_pump,
        )
        self._btn_pump.pack(side=LEFT, padx=3)

        Button(
            self,
            text='Purge Valve',
            command=self.on_purge_valve,
        ).pack(side=LEFT, padx=3)

    def on_home_robot(self) -> None:
        '''
            Handles click event on home robot button.

            :exceptions: None.
        '''
        self._action_delegate.on_home_robot()

    def on_toggle_pump(self) -> None:
        '''
            Handles click event on toggle pump button.

            :exceptions: None.
        '''
        active: bool = self._action_delegate.on_toggle_pump()
        self.set_pump_active(active)

    def on_purge_valve(self) -> None:
        '''
            Handles click event on purge valve button.

            :exceptions: None.
        '''
        self._action_delegate.on_purge_valve()

    def set_pump_active(self, active: bool) -> None:
        '''
            Updates vacuum pump button text according to active state.

            :param active: True if pump is active, False otherwise.
            :exceptions: None.
        '''
        self._btn_pump.configure(
            text='Pump: ON' if active else 'Pump: OFF'
        )
