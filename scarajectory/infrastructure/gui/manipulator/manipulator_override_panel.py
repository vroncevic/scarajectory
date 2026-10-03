# -*- coding: UTF-8 -*-

'''
Module
    manipulator_override_panel.py
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
    Manipulator manual override, homing, vacuum pump and purge valve control panel.
'''

from __future__ import annotations

from tkinter import LEFT, Widget, X
from tkinter.ttk import Button, Frame, Label, Scale
from typing import Final

from scarajectory.infrastructure.gui.manipulator.null_manipulator_action_delegate import NullManipulatorActionDelegate
from scarajectory.infrastructure.gui.manipulator.imanipulator_action_delegate import IManipulatorActionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

NULL_MANIPULATOR_DELEGATE: Final[IManipulatorActionDelegate] = (
    NullManipulatorActionDelegate()
)


class ManipulatorOverridePanel(Frame):
    '''
        Subcomponent providing speed override scale, robot homing and pneumatic valve toggles.

        It defines:

            :attributes:
                | _override_slider - Feedrate speed override scale widget.
                | _lbl_override - Percentage readout label for speed override.
                | _btn_pump - Toggle button widget for vacuum pump control.
                | _action_delegate - Action delegate handling manipulator actuation commands.
            :methods:
                | __init__ - Initializes override and actuator panel layout.
                | set_action_delegate - Injects active action delegate for manipulator commands.
                | on_home_robot - Handles click event on home robot button.
                | on_toggle_pump - Handles click event on toggle pump button.
                | on_purge_valve - Handles click event on purge valve button.
                | handle_slider_change - Handles slider movement and dispatches integer percentage.
                | set_override_label - Updates percentage readout label for speed override.
                | set_pump_active - Updates pump button text according to active state.
                | set_pump_state - Compatibility wrapper updating pump button text.
    '''

    _override_slider: Scale
    _lbl_override: Label
    _btn_pump: Button
    _action_delegate: IManipulatorActionDelegate

    def __init__(
        self,
        parent: Widget,
        *,
        action_delegate: IManipulatorActionDelegate = NULL_MANIPULATOR_DELEGATE,
    ) -> None:
        '''
            Initializes override and actuator panel layout.

            :param parent: Parent container widget.
            :param action_delegate: Injected IManipulatorActionDelegate action delegate.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._action_delegate = action_delegate

        action_box: Frame = Frame(self)
        action_box.pack(fill=X, pady=2)
        Button(
            action_box,
            text='Home Robot',
            command=self.on_home_robot,
        ).pack(side=LEFT, padx=3)
        self._btn_pump = Button(
            action_box,
            text='Pump: OFF',
            command=self.on_toggle_pump,
        )
        self._btn_pump.pack(side=LEFT, padx=3)
        Button(
            action_box,
            text='Purge Valve',
            command=self.on_purge_valve,
        ).pack(side=LEFT, padx=3)

        override_box: Frame = Frame(self)
        override_box.pack(fill=X, pady=2)
        Label(override_box, text='Feedrate Override:').pack(side=LEFT, padx=(3, 2))
        self._lbl_override = Label(override_box, text='100%', width=5)
        self._override_slider = Scale(
            override_box,
            from_=10,
            to=200,
            value=100,
            command=self.handle_slider_change,
        )
        self._override_slider.pack(side=LEFT, fill=X, expand=True, padx=4)
        self._lbl_override.pack(side=LEFT, padx=2)

    def set_action_delegate(
        self,
        action_delegate: IManipulatorActionDelegate,
    ) -> None:
        '''
            Injects active action delegate for manipulator commands.

            :param action_delegate: IManipulatorActionDelegate instance.
            :exceptions: None.
        '''
        self._action_delegate = action_delegate

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
        self._action_delegate.on_toggle_pump()

    def on_purge_valve(self) -> None:
        '''
            Handles click event on purge valve button.

            :exceptions: None.
        '''
        self._action_delegate.on_purge_valve()

    def handle_slider_change(self, val: str) -> None:
        '''
            Handles slider movement and dispatches integer percentage.

            :param val: Slider position value string.
            :exceptions: None.
        '''
        pct: int = max(10, min(200, int(float(val))))
        self.set_override_label(pct)
        self._action_delegate.on_override_change(pct)

    def set_override_label(self, pct: int) -> None:
        '''
            Updates percentage readout label for speed override.

            :param pct: Speed override percentage (10 to 200).
            :exceptions: None.
        '''
        self._lbl_override.configure(text=f'{pct}%')

    def set_pump_active(self, active: bool) -> None:
        '''
            Updates pump button text according to active state.

            :param active: True if pump is active, False otherwise.
            :exceptions: None.
        '''
        self._btn_pump.configure(text='Pump: ON' if active else 'Pump: OFF')

    def set_pump_state(self, active: bool) -> None:
        '''
            Compatibility wrapper updating pump button text according to active state.

            :param active: True if pump is active, False otherwise.
            :exceptions: None.
        '''
        self.set_pump_active(active)

    @property
    def pump_button_text(self) -> str:
        '''
            Returns text of pump toggle button.

            :return: Button label text.
            :exceptions: None.
        '''
        return str(self._btn_pump['text'])

    @property
    def override_text(self) -> str:
        '''
            Returns text of feedrate override readout label.

            :return: Label text string.
            :exceptions: None.
        '''
        return str(self._lbl_override['text'])
