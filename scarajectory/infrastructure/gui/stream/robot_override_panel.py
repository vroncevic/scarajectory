# -*- coding: UTF-8 -*-

'''
Module
    robot_override_panel.py
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
    Robot manual override, homing, vacuum pump and purge valve control panel.
'''

from __future__ import annotations

from collections.abc import Callable
from tkinter import LEFT, Widget, X
from tkinter.ttk import Button, Frame, Label, Scale
from typing import Final

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class RobotOverridePanel(Frame):
    '''
        Subcomponent providing speed override scale, robot homing and pneumatic valve toggles.

        It defines:

            :attributes:
                | _override_slider - Feedrate speed override scale widget.
                | _lbl_override - Percentage readout label for speed override.
                | _btn_pump - Toggle button widget for vacuum pump control.
                | _on_override_change - Callback for feedrate slider changes.
            :methods:
                | __init__ - Initializes override and actuator panel layout.
                | set_pump_state - Updates pump button text according to active state.
                | _handle_slider_change - Handles slider movement and dispatches integer percentage.
    '''

    _override_slider: Scale
    _lbl_override: Label
    _btn_pump: Button
    _on_override_change: Callable[[int], None]

    def __init__(
        self,
        parent: Widget,
        *,
        on_home: Callable[[], None],
        on_toggle_pump: Callable[[], None],
        on_purge_valve: Callable[[], None],
        on_override_change: Callable[[int], None],
        **kwargs: object,
    ) -> None:
        '''
            Initializes override and actuator panel layout.

            :param parent: Parent container widget.
            :param on_home: Callback for homing calibration command.
            :param on_toggle_pump: Callback for toggling vacuum pump.
            :param on_purge_valve: Callback for pulsing purge valve.
            :param on_override_change: Callback invoked on speed override changes.
            :exceptions: None.
        '''
        super().__init__(parent, **kwargs)
        self._on_override_change: Final[Callable[[int], None]] = on_override_change

        action_box: Frame = Frame(self)
        action_box.pack(fill=X, pady=2)
        Button(action_box, text='Home Robot', command=on_home).pack(side=LEFT, padx=3)
        self._btn_pump = Button(action_box, text='Pump: OFF', command=on_toggle_pump)
        self._btn_pump.pack(side=LEFT, padx=3)
        Button(action_box, text='Purge Valve', command=on_purge_valve).pack(side=LEFT, padx=3)

        override_box: Frame = Frame(self)
        override_box.pack(fill=X, pady=2)
        Label(override_box, text='Feedrate Override:').pack(side=LEFT, padx=(3, 2))
        self._lbl_override = Label(override_box, text='100%', width=5)
        self._override_slider = Scale(
            override_box,
            from_=10,
            to=200,
            value=100,
            command=self._handle_slider_change,
        )
        self._override_slider.pack(side=LEFT, fill=X, expand=True, padx=4)
        self._lbl_override.pack(side=LEFT, padx=2)

    def _handle_slider_change(self, val: str) -> None:
        '''
            Handles slider movement and dispatches integer percentage.

            :param val: Slider position value string.
            :exceptions: None.
        '''
        pct: int = max(10, min(200, int(float(val))))
        self._lbl_override.configure(text=f'{pct}%')
        self._on_override_change(pct)

    def set_pump_state(self, active: bool) -> None:
        '''
            Updates pump button text according to active state.

            :param active: True if pump is active, False otherwise.
            :exceptions: None.
        '''
        self._btn_pump.configure(text='Pump: ON' if active else 'Pump: OFF')
