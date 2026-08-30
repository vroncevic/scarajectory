# -*- coding: UTF-8 -*-

'''
Module
    jog_tab.py
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
    Manual Jog control tab for direct Cartesian and joint manipulation.
'''

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Final

from scarajectory.core.service.itrajectory_streamer import ITrajectoryStreamer
from scarajectory.infrastructure.communication.protocol.command_formatter import CommandFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogTab(ttk.Frame):
    '''
        Manual jog tab for Cartesian motion, actuator toggles and raw serial commands.

        It defines:

            :attributes:
                | _streamer - Robot communication and streaming service.
                | _step_var - Selected jog step increment in mm.
                | _entry_raw - Text entry for raw ASCII micro-commands.
            :methods:
                | __init__ - Initializes manual jog controls.
                | jog_step - Sends relative jog step along specified axis.
                | send_raw - Transmits text command from entry field.
    '''

    _streamer: Final[ITrajectoryStreamer]
    _step_var: tk.DoubleVar
    _entry_raw: ttk.Entry

    def __init__(self, parent: tk.Widget, streamer: ITrajectoryStreamer, **kwargs: object) -> None:
        '''
            Initializes manual jog controls.

            :param parent: Parent notebook widget.
            :param streamer: ITrajectoryStreamer instance.
            :exceptions: None.
        '''
        super().__init__(parent, padding=6, **kwargs)  # type: ignore[arg-type]
        self._streamer = streamer
        self._step_var = tk.DoubleVar(value=10.0)
        self._build_layout()

    def _build_layout(self) -> None:
        '''
            Constructs power, jog grid, auxiliary toggles and raw command inputs.

            :exceptions: None.
        '''
        pwr_f: ttk.Frame = ttk.Frame(self)
        pwr_f.pack(fill=tk.X, pady=2)
        ttk.Button(
            pwr_f,
            text='⚡ Enable Robot',
            style='Success.TButton',
            command=lambda: self._streamer.send_raw_command(CommandFormatter.format_enable())
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            pwr_f,
            text='🛑 Disable',
            command=lambda: self._streamer.send_raw_command(CommandFormatter.format_disable())
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            pwr_f,
            text='🏠 Home All',
            command=lambda: self._streamer.send_raw_command(CommandFormatter.format_home())
        ).pack(side=tk.LEFT, padx=2)

        step_f: ttk.Frame = ttk.Frame(self)
        step_f.pack(fill=tk.X, pady=4)
        ttk.Label(step_f, text='Step (mm):').pack(side=tk.LEFT)
        for s in (1.0, 5.0, 10.0, 25.0):
            ttk.Radiobutton(step_f, text=f'{int(s)}', value=s, variable=self._step_var).pack(side=tk.LEFT, padx=2)

        grid_f: ttk.Frame = ttk.Frame(self)
        grid_f.pack(fill=tk.X, pady=2)
        ttk.Button(grid_f, text='▲ +Y', width=6, command=lambda: self.jog_step('Y', 1.0)).grid(row=0, column=1, padx=2, pady=1)
        ttk.Button(grid_f, text='◀ -X', width=6, command=lambda: self.jog_step('X', -1.0)).grid(row=1, column=0, padx=2, pady=1)
        ttk.Button(grid_f, text='▶ +X', width=6, command=lambda: self.jog_step('X', 1.0)).grid(row=1, column=2, padx=2, pady=1)
        ttk.Button(grid_f, text='▼ -Y', width=6, command=lambda: self.jog_step('Y', -1.0)).grid(row=2, column=1, padx=2, pady=1)

        ttk.Button(grid_f, text='▲ +Z', width=6, command=lambda: self.jog_step('Z', 1.0)).grid(row=0, column=4, padx=6, pady=1)
        ttk.Button(grid_f, text='▼ -Z', width=6, command=lambda: self.jog_step('Z', -1.0)).grid(row=2, column=4, padx=6, pady=1)
        ttk.Button(grid_f, text='↺ -Phi', width=6, command=lambda: self.jog_step('Phi', -1.0)).grid(row=1, column=3, padx=2, pady=1)
        ttk.Button(grid_f, text='↻ +Phi', width=6, command=lambda: self.jog_step('Phi', 1.0)).grid(row=1, column=5, padx=2, pady=1)

        aux_f: ttk.Frame = ttk.Frame(self)
        aux_f.pack(fill=tk.X, pady=4)
        ttk.Button(
            aux_f,
            text='Pump ON',
            command=lambda: self._streamer.send_raw_command(CommandFormatter.format_pump(True))
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            aux_f,
            text='Pump OFF',
            command=lambda: self._streamer.send_raw_command(CommandFormatter.format_pump(False))
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            aux_f,
            text='Valve ON',
            command=lambda: self._streamer.send_raw_command(CommandFormatter.format_valve(True))
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            aux_f,
            text='Valve OFF',
            command=lambda: self._streamer.send_raw_command(CommandFormatter.format_valve(False))
        ).pack(side=tk.LEFT, padx=2)

        raw_f: ttk.Frame = ttk.Frame(self)
        raw_f.pack(fill=tk.X, pady=2)
        ttk.Label(raw_f, text='Raw:').pack(side=tk.LEFT)
        self._entry_raw = ttk.Entry(raw_f, width=20)
        self._entry_raw.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        self._entry_raw.bind('<Return>', lambda e: self.send_raw())
        ttk.Button(raw_f, text='Send', command=self.send_raw).pack(side=tk.LEFT)

    def jog_step(self, axis: str, sign: float = 1.0) -> None:
        '''
            Sends relative jog command based on selected step size.

            :param axis: Axis identifier ('X', 'Y', 'Z', 'Phi').
            :param sign: Direction multiplier (+1.0 or -1.0).
            :exceptions: None.
        '''
        delta: float = self._step_var.get() * sign
        cmd: str = CommandFormatter.format_jog(axis, delta)
        self._streamer.send_raw_command(cmd)
        self._streamer.send_raw_command(CommandFormatter.format_status())

    def send_raw(self) -> None:
        '''
            Transmits raw command from text input to microcontroller.

            :exceptions: None.
        '''
        cmd: str = self._entry_raw.get().strip()
        if cmd:
            self._streamer.send_raw_command(cmd)
            self._entry_raw.delete(0, tk.END)
