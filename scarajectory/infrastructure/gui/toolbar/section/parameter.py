# -*- coding: UTF-8 -*-

'''
Module
    parameter.py
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
    Subcomponent managing waypoint defaults and reach limit enforcement.
'''

from __future__ import annotations

from tkinter import BooleanVar, LEFT, VERTICAL, Widget, Y
from tkinter.ttk import Checkbutton, Frame, Label, Separator, Spinbox
from typing import Final

from scarajectory.infrastructure.gui.canvas.icanvas import ICanvas
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ParameterSection(Frame):
    '''
        Subcomponent managing waypoint default Z elevation, speed, and reach limit.

        It defines:

            :attributes:
                | _canvas - Active CAD canvas interface.
                | _reach_limits - Minimum and maximum reach distance in mm.
                | _settings - Active canvas creation parameters.
                | _spin_z - Default waypoint Z elevation spinbox.
                | _spin_speed - Default waypoint feedrate spinbox.
                | _deadzone_var - Deadzone kinematic boundary lock variable.
            :methods:
                | __init__ - Initializes parameter controls.
                | build_layout - Builds spinboxes and reach limit checkbutton.
                | on_defaults_changed - Applies updated defaults to canvas.
                | set_deadzone - Sets deadzone enforcement checkbox state.
    '''

    _canvas: ICanvas
    _reach_limits: tuple[float, float]
    _settings: CanvasSettings
    _spin_z: Spinbox
    _spin_speed: Spinbox
    _deadzone_var: BooleanVar

    def __init__(
        self,
        parent: Widget,
        *,
        canvas: ICanvas,
        reach_limits: tuple[float, float],
        settings: CanvasSettings,
    ) -> None:
        '''
            Initializes parameter controls.

            :param parent: Parent container widget.
            :param canvas: Active CAD canvas interface.
            :param reach_limits: Tuple of minimum and maximum reach radius in mm.
            :param settings: Active canvas creation parameters.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._canvas: Final[ICanvas] = canvas
        self._reach_limits: Final[tuple[float, float]] = reach_limits
        self._settings: Final[CanvasSettings] = settings
        self.build_layout()

    def build_layout(self) -> None:
        '''
            Builds spinboxes and reach limit checkbutton.

            :exceptions: None.
        '''
        Label(self, text='Z (mm):').pack(side=LEFT, padx=2)
        self._spin_z = Spinbox(
            self, from_=0.0, to=100.0, increment=5.0, width=5
        )
        self._spin_z.set(f'{self._settings.default_z:.1f}')
        self._spin_z.pack(side=LEFT, padx=2)
        self._spin_z.bind('<FocusOut>', lambda e: self.on_defaults_changed())
        self._spin_z.bind('<Return>', lambda e: self.on_defaults_changed())

        Label(self, text='Speed:').pack(side=LEFT, padx=4)
        self._spin_speed = Spinbox(
            self, from_=1.0, to=200.0, increment=10.0, width=5
        )
        self._spin_speed.set(f'{self._settings.default_speed:.1f}')
        self._spin_speed.pack(side=LEFT, padx=2)
        self._spin_speed.bind(
            '<FocusOut>', lambda e: self.on_defaults_changed()
        )
        self._spin_speed.bind('<Return>', lambda e: self.on_defaults_changed())

        Separator(self, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=8)
        self._deadzone_var = BooleanVar(
            value=self._settings.enforce_deadzone
        )
        r_min, r_max = self._reach_limits
        reach_text: str = f'Enforce Reach Limits ({r_min:.0f}-{r_max:.0f}mm)'
        Checkbutton(
            self,
            text=reach_text,
            variable=self._deadzone_var,
            command=self.on_defaults_changed,
        ).pack(side=LEFT, padx=3)

    def on_defaults_changed(self) -> None:
        '''
            Applies updated defaults from spinboxes to canvas.

            :exceptions: None.
        '''
        try:
            dz: float = float(self._spin_z.get())
            dsp: float = float(self._spin_speed.get())
            enforce: bool = self._deadzone_var.get()
            self._canvas.update_settings(
                CanvasSettings(
                    default_z=dz,
                    default_speed=dsp,
                    enforce_deadzone=enforce,
                )
            )
        except ValueError:
            pass

    def set_deadzone(self, enabled: bool) -> None:
        '''
            Sets deadzone enforcement checkbox state.

            :param enabled: True to enforce deadzone, False to disable.
            :exceptions: None.
        '''
        self._deadzone_var.set(enabled)
        self.on_defaults_changed()
