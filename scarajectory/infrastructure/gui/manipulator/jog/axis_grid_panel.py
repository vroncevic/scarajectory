# -*- coding: UTF-8 -*-

'''
Module
    axis_grid_panel.py
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
    Directional axis jog grid and step size selection subcomponent.
'''

from __future__ import annotations

from tkinter import DoubleVar, LEFT, Widget, X
from tkinter.ttk import Button, Frame, Label, Radiobutton
from typing import Final

from scarajectory.core.model.jog.jog_axis import JogAxis
from scarajectory.core.service.manipulator.ijog_controller import IJogController
from scarajectory.core.service.manipulator.iquery_controller import IQueryController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogAxisGridPanel(Frame):
    '''
        Panel providing directional jog buttons and step increment configuration.

        It defines:

            :attributes:
                | _jog_controller - Injected relative axis movement controller.
                | _query_controller - Injected robot state inquiry controller.
                | _step_var - Selected jog step increment variable in mm.
            :methods:
                | __init__ - Initializes directional jog grid and step selector.
                | jog_step - Sends relative jog step along specified axis.
                | get_step_size - Returns currently selected step size in mm.
                | set_step_size - Configures active jog step size in mm.
    '''

    _jog_controller: IJogController
    _query_controller: IQueryController
    _step_var: DoubleVar

    def __init__(
        self,
        parent: Widget,
        *,
        jog_controller: IJogController,
        query_controller: IQueryController,
    ) -> None:
        '''
            Initializes directional jog grid and step selector layout.

            :param parent: Parent container widget.
            :param jog_controller: Injected relative axis movement controller.
            :param query_controller: Injected robot state inquiry controller.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._jog_controller: Final[IJogController] = jog_controller
        self._query_controller: Final[IQueryController] = query_controller
        self._step_var = DoubleVar(value=10.0)

        # Step size selectors
        step_frame: Frame = Frame(self)
        step_frame.pack(fill=X, pady=3)
        Label(step_frame, text='Step Size (mm):').pack(side=LEFT, padx=(0, 6))

        for step in (0.5, 1.0, 5.0, 10.0, 20.0):
            Radiobutton(
                step_frame,
                text=str(step),
                variable=self._step_var,
                value=step,
            ).pack(side=LEFT, padx=3)

        # 3x3 Grid of directional step buttons
        grid_frame: Frame = Frame(self)
        grid_frame.pack(pady=4)

        # Row 0: (+X, -Y diagonal left), (+Y up), (+X, +Y diagonal right)
        Button(
            grid_frame,
            text='Y+',
            width=6,
            command=lambda: self.jog_step(JogAxis.Y, 1.0),
        ).grid(row=0, column=1, padx=2, pady=2)

        # Row 1: (-X left), (Z+ up), (+X right)
        Button(
            grid_frame,
            text='X-',
            width=6,
            command=lambda: self.jog_step(JogAxis.X, -1.0),
        ).grid(row=1, column=0, padx=2, pady=2)
        Button(
            grid_frame,
            text='Z+',
            width=6,
            command=lambda: self.jog_step(JogAxis.Z, 1.0),
        ).grid(row=1, column=1, padx=2, pady=2)
        Button(
            grid_frame,
            text='X+',
            width=6,
            command=lambda: self.jog_step(JogAxis.X, 1.0),
        ).grid(row=1, column=2, padx=2, pady=2)

        # Row 2: (-Y down), (Z- down)
        Button(
            grid_frame,
            text='Y-',
            width=6,
            command=lambda: self.jog_step(JogAxis.Y, -1.0),
        ).grid(row=2, column=1, padx=2, pady=2)
        Button(
            grid_frame,
            text='Z-',
            width=6,
            command=lambda: self.jog_step(JogAxis.Z, -1.0),
        ).grid(row=2, column=2, padx=2, pady=2)

    def jog_step(self, axis: JogAxis | str, sign: float = 1.0) -> None:
        '''
            Sends relative jog step along specified axis and polls hardware status.

            :param axis: Targeted JogAxis enum value or string name.
            :param sign: Step sign multiplier (+1.0 or -1.0).
            :exceptions: None.
        '''
        axis_name: str = axis.value if isinstance(axis, JogAxis) else str(axis)
        step: float = self._step_var.get() * sign
        self._jog_controller.jog(axis_name, step)
        self._query_controller.query_status()

    def get_step_size(self) -> float:
        '''
            Returns currently selected step size in mm.

            :return: Step size in millimeters.
            :exceptions: None.
        '''
        return self._step_var.get()

    def set_step_size(self, size: float) -> None:
        '''
            Configures active jog step size in mm.

            :param size: Step increment in millimeters.
            :exceptions: None.
        '''
        self._step_var.set(size)
