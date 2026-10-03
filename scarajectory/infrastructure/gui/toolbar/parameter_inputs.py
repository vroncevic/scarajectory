# -*- coding: UTF-8 -*-

'''
Module
    parameter_inputs.py
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
    Subcomponent managing defaults, reach toggle and cursor monitor.
'''

from __future__ import annotations

from tkinter import BooleanVar, LEFT, RIGHT, VERTICAL, Widget, Y
from tkinter.ttk import Checkbutton, Frame, Label, Separator, Spinbox
from typing import Final

from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.toolbar.parameter_inputs_bundle import ParameterInputsBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolbarParameterInputs(Frame):
    '''
        Subcomponent managing waypoint defaults, reach limit and cursor.

        It defines:

            :attributes:
                | _bundle - Injected ParameterInputsBundle containing collaborators and settings.
                | _spin_z - Default waypoint Z elevation spinbox.
                | _spin_speed - Default waypoint feedrate spinbox.
                | _deadzone_var - Deadzone kinematic boundary lock variable.
                | _lbl_cursor - Dynamic cursor coordinate and zoom label.
            :methods:
                | __init__ - Initializes parameter controls.
                | build_layout - Builds spinboxes, deadzone and cursor monitor.
                | on_defaults_changed - Applies updated defaults to canvas.
                | set_deadzone - Sets deadzone enforcement checkbox state.
                | get_cursor_label - Returns cursor info label widget.
    '''

    _bundle: ParameterInputsBundle
    _spin_z: Spinbox
    _spin_speed: Spinbox
    _deadzone_var: BooleanVar
    _lbl_cursor: Label

    def __init__(
        self,
        parent: Widget,
        bundle: ParameterInputsBundle,
    ) -> None:
        '''
            Initializes parameter controls.

            :param parent: Parent container widget.
            :param bundle: ParameterInputsBundle containing dependencies and bounds.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._bundle: Final[ParameterInputsBundle] = bundle
        self.build_layout()

    def build_layout(self) -> None:
        '''
            Builds spinboxes, deadzone toggle and cursor monitor.

            :exceptions: None.
        '''
        Label(self, text='Z (mm):').pack(side=LEFT, padx=2)
        self._spin_z = Spinbox(
            self, from_=0.0, to=100.0, increment=5.0, width=5
        )
        self._spin_z.set(f'{self._bundle.settings.default_z:.1f}')
        self._spin_z.pack(side=LEFT, padx=2)
        self._spin_z.bind('<FocusOut>', lambda e: self.on_defaults_changed())
        self._spin_z.bind('<Return>', lambda e: self.on_defaults_changed())

        Label(self, text='Speed:').pack(side=LEFT, padx=4)
        self._spin_speed = Spinbox(
            self, from_=1.0, to=200.0, increment=10.0, width=5
        )
        self._spin_speed.set(f'{self._bundle.settings.default_speed:.1f}')
        self._spin_speed.pack(side=LEFT, padx=2)
        self._spin_speed.bind(
            '<FocusOut>', lambda e: self.on_defaults_changed()
        )
        self._spin_speed.bind('<Return>', lambda e: self.on_defaults_changed())

        Separator(self, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=8)
        self._deadzone_var = BooleanVar(
            value=self._bundle.settings.enforce_deadzone
        )
        reach_text: str = (
            f'Enforce Reach Limits ({self._bundle.r_min:.0f}-{self._bundle.r_max:.0f}mm)'
        )
        Checkbutton(
            self,
            text=reach_text,
            variable=self._deadzone_var,
            command=self.on_defaults_changed,
        ).pack(side=LEFT, padx=3)

        self._lbl_cursor = Label(
            self,
            text='Cursor: X=  0.0 mm | Y=  0.0 mm | R=  0.0 mm | Zoom: 100%',
            font=('DejaVu Sans Mono', 9),
        )
        self._lbl_cursor.pack(side=RIGHT, padx=8)
        self._bundle.status_presenter.set_hover_label(self._lbl_cursor)

    def on_defaults_changed(self) -> None:
        '''
            Applies updated defaults from spinboxes to canvas.

            :exceptions: None.
        '''
        try:
            dz: float = float(self._spin_z.get())
            dsp: float = float(self._spin_speed.get())
            enforce: bool = self._deadzone_var.get()
            self._bundle.canvas.update_settings(
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

    def get_cursor_label(self) -> Label:
        '''
            Returns cursor info label widget.

            :return: Label widget displaying coordinates and zoom.
            :exceptions: None.
        '''
        return self._lbl_cursor
