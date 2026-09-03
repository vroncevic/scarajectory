# -*- coding: UTF-8 -*-

'''
Module
    streamer_tab.py
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
    Hardware serial streamer tab with progress monitoring and terminal logs.
'''

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Final

from scarajectory.core.model.stream_config_dto import StreamConfigDTO
from scarajectory.core.model.stream_progress import StreamProgress
from scarajectory.core.model.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.service.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.itrajectory_streamer import ITrajectoryStreamer
from scarajectory.infrastructure.communication.serial_port_scanner import SerialPortScanner
from scarajectory.infrastructure.communication.serial_device_preferences import SerialDevicePreferences
from scarajectory.infrastructure.gui.components.serial_console import SerialConsole
from scarajectory.infrastructure.gui.components.stream_status_bar import StreamStatusBar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamerTab(ttk.Frame):
    '''
        Hardware connection and trajectory streaming tab.

        It defines:

            :attributes:
                | _plan - Active trajectory plan domain abstraction.
                | _validator - Kinematic reachability validator.
                | _streamer - Robot communication and streaming service.
                | _cbo_ports - Serial port selection combobox.
                | _btn_connect - Connect/disconnect action button.
                | _status_bar - Progress bar and summary readout widget.
                | _console - Serial communication terminal output component.
            :methods:
                | __init__ - Initializes the streamer tab panel.
                | refresh_ports - Scans available serial/USB ports on the host.
                | append_log - Appends message to terminal log console.
                | update_progress - Updates streamer progress bar and metrics.
    '''

    _plan: ITrajectoryPlan
    _validator: ITrajectoryValidator
    _streamer: ITrajectoryStreamer
    _cbo_ports: ttk.Combobox
    _btn_connect: ttk.Button
    _status_bar: StreamStatusBar
    _console: SerialConsole

    def __init__(
        self,
        parent: tk.Widget,
        plan: ITrajectoryPlan,
        validator: ITrajectoryValidator,
        streamer: ITrajectoryStreamer,
        **kwargs: object
    ) -> None:
        '''
            Initializes the streamer tab panel.

            :param parent: Parent notebook widget.
            :param plan: Active ITrajectoryPlan.
            :param validator: ITrajectoryValidator instance.
            :param streamer: ITrajectoryStreamer instance.
            :exceptions: None.
        '''
        super().__init__(parent, padding=6, **kwargs)
        self._plan: Final[ITrajectoryPlan] = plan
        self._validator: Final[ITrajectoryValidator] = validator
        self._streamer: Final[ITrajectoryStreamer] = streamer
        self._build_layout()
        self.refresh_ports()

    def _build_layout(self) -> None:
        '''
            Constructs hardware serial connection and streaming widgets.

            :exceptions: None.
        '''
        port_box: ttk.Frame = ttk.Frame(self)
        port_box.pack(fill=tk.X, pady=2)
        ttk.Label(port_box, text='Port:').pack(side=tk.LEFT)
        self._cbo_ports = ttk.Combobox(port_box, width=16)
        self._cbo_ports.pack(side=tk.LEFT, padx=4)
        self._cbo_ports.bind('<<ComboboxSelected>>', lambda e: self._save_active_pref())
        ttk.Button(port_box, text='Refresh', command=self.refresh_ports).pack(side=tk.LEFT, padx=2)

        self._btn_connect = ttk.Button(port_box, text='Connect', style='Accent.TButton', command=self._on_toggle_connect)
        self._btn_connect.pack(side=tk.LEFT, padx=6)

        ctrl_box: ttk.Frame = ttk.Frame(self)
        ctrl_box.pack(fill=tk.X, pady=4)
        ttk.Button(ctrl_box, text='Stream to Robot', style='Success.TButton', command=self._on_start_stream).pack(side=tk.LEFT, padx=3)
        ttk.Button(ctrl_box, text='Pause / Resume', command=self._on_pause_resume_stream).pack(side=tk.LEFT, padx=3)
        ttk.Button(ctrl_box, text='Stop / E-STOP', style='Danger.TButton', command=self._streamer.stop_streaming).pack(side=tk.LEFT, padx=3)

        self._status_bar = StreamStatusBar(self)
        self._status_bar.pack(fill=tk.X, pady=2)

        self._console = SerialConsole(self)
        self._console.pack(fill=tk.BOTH, expand=True, pady=2)

    def refresh_ports(self) -> None:
        '''
            Scans and lists active serial / tty ports on the host system.

            :exceptions: None.
        '''
        current_selection: str = self._cbo_ports.get()
        saved_port, _ = SerialDevicePreferences.load_preference()
        ports = SerialPortScanner.scan_ports()
        self._cbo_ports['values'] = ports

        if current_selection in ports:
            self._cbo_ports.set(current_selection)
        elif saved_port:
            matched_port = next((p for p in ports if p.startswith(saved_port)), None)
            if matched_port:
                self._cbo_ports.set(matched_port)
            elif ports:
                self._cbo_ports.current(0)
            else:
                self._cbo_ports.set('')
        elif ports:
            self._cbo_ports.current(0)
        else:
            self._cbo_ports.set('')

    def append_log(self, text: str, is_outgoing: bool = False) -> None:
        '''
            Appends timestamped message to the terminal console widget.

            :param text: Message string.
            :param is_outgoing: True if transmitted command.
            :exceptions: None.
        '''
        self._console.append_log(text, is_outgoing)

        if 'Connection lost' in text or 'Disconnected from' in text:
            self._btn_connect.configure(text='Connect', style='Accent.TButton')
            self._status_bar.set_status_text('Streamer: Disconnected')

    def update_progress(self, progress: StreamProgress) -> None:
        '''
            Updates progress bar and streaming status indicator widgets.

            :param progress: StreamProgress data model.
            :exceptions: None.
        '''
        self._status_bar.update_progress(progress)

    def _save_active_pref(self) -> None:
        '''
            Persists selected serial device port to storage.

            :exceptions: None.
        '''
        port_val: str = self._cbo_ports.get()
        if port_val:
            port: str = port_val.split(' ')[0] if ' ' in port_val else port_val
            SerialDevicePreferences.save_preference(port, 115200)

    def _on_toggle_connect(self) -> None:
        '''
            Connects or disconnects from selected serial port.

            :exceptions: None.
        '''
        if self._streamer.is_connected():
            self._streamer.disconnect()
            self._btn_connect.configure(text='Connect', style='Accent.TButton')
            self._status_bar.set_status_text('Streamer: Disconnected')
        else:
            port_val: str = self._cbo_ports.get()
            if not port_val:
                messagebox.showerror('Serial Port Error', 'No serial port selected.')
                return

            port: str = port_val.split(' ')[0] if ' ' in port_val else port_val
            config: StreamConfigDTO = StreamConfigDTO(port=port, baudrate=115200, timeout=0.1)
            if self._streamer.connect_with_config(config):
                self._save_active_pref()
                self._btn_connect.configure(text='Disconnect', style='Danger.TButton')
                self._status_bar.set_status_text(f'Streamer: Connected to {port}')

    def _on_start_stream(self) -> None:
        '''
            Starts streaming trajectory after validation check.

            :exceptions: None.
        '''
        valid, msgs = self._validator.validate_plan(self._plan)
        if not valid:
            res: bool = messagebox.askyesno(
                'Validation Warnings',
                'Plan has validation warnings/errors:\n\n' + '\n'.join(msgs[:4]) + '\n\nDo you want to proceed anyway?'
            )
            if not res:
                return

        if not self._streamer.start_streaming(self._plan.waypoints):
            messagebox.showerror('Stream Error', 'Failed to start stream. Check serial connection.')

    def _on_pause_resume_stream(self) -> None:
        '''
            Toggles stream pause/resume.

            :exceptions: None.
        '''
        try:
            self._streamer.pause_streaming()
        except (AttributeError, RuntimeError):
            self._streamer.resume_streaming()
