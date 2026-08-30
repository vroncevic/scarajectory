# -*- coding: UTF-8 -*-

'''
Module
    controls.py
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
    Tabbed control notebook housing Serial Streamer, Validator, Jog and Program preview.
'''

from __future__ import annotations

import glob
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Final

import serial.tools.list_ports

from scarajectory.core.model.stream_config_dto import StreamConfigDTO
from scarajectory.core.model.stream_progress import StreamProgress
from scarajectory.core.model.stream_state import StreamState
from scarajectory.core.model.trajectory_metrics import TrajectoryMetrics
from scarajectory.core.service.iservice import IService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControlsPanel(ttk.Frame):
    '''
        Tabbed controller housing Serial Streamer, Validation, Jog and Program preview panels.

        It defines:

            :attributes:
                | _service - Core IService instance.
                | _notebook - Multi-tab notebook container.
            :methods:
                | __init__ - Initializes tabbed control panels.
                | refresh_ports - Updates available serial ports list with USB devices prioritized.
                | append_log - Appends message to terminal log console.
                | update_progress - Updates streamer progress bar and metrics.
    '''

    _service: Final[IService]
    _notebook: ttk.Notebook
    _cbo_ports: ttk.Combobox
    _btn_connect: ttk.Button
    _btn_stream: ttk.Button
    _btn_pause: ttk.Button
    _btn_stop: ttk.Button
    _progress_var: tk.DoubleVar
    _progress_bar: ttk.Progressbar
    _lbl_stream_status: ttk.Label
    _txt_log: tk.Text
    _txt_val: tk.Text
    _txt_preview: tk.Text
    _step_var: tk.DoubleVar
    _entry_raw: ttk.Entry

    def __init__(self, parent: tk.Widget, service: IService, **kwargs: object) -> None:
        '''
            Initializes tabbed control panels.

            :param parent: Parent container widget.
            :param service: Core IService instance.
            :exceptions: None.
        '''
        super().__init__(parent, **kwargs)  # type: ignore[arg-type]
        self._service = service
        self._step_var = tk.DoubleVar(value=10.0)
        self._build_tabs()
        self.refresh_ports()

    def _build_tabs(self) -> None:
        '''
            Constructs tab pages for Streamer, Validation, Jog, and Preview.

            :exceptions: None.
        '''
        self._notebook = ttk.Notebook(self)
        self._notebook.pack(fill=tk.BOTH, expand=True)

        self._build_streamer_tab()
        self._build_validation_tab()
        self._build_jog_tab()
        self._build_preview_tab()

    def _build_streamer_tab(self) -> None:
        '''
            Constructs hardware serial connection and streaming panel.

            :exceptions: None.
        '''
        tab: ttk.Frame = ttk.Frame(self._notebook, padding=6)
        self._notebook.add(tab, text=' Hardware Streamer ')

        port_box: ttk.Frame = ttk.Frame(tab)
        port_box.pack(fill=tk.X, pady=2)
        ttk.Label(port_box, text='Port:').pack(side=tk.LEFT)
        self._cbo_ports = ttk.Combobox(port_box, width=16)
        self._cbo_ports.pack(side=tk.LEFT, padx=4)
        ttk.Button(port_box, text='Refresh', command=self.refresh_ports).pack(side=tk.LEFT, padx=2)

        self._btn_connect = ttk.Button(port_box, text='Connect', style='Accent.TButton', command=self._on_toggle_connect)
        self._btn_connect.pack(side=tk.LEFT, padx=6)

        ctrl_box: ttk.Frame = ttk.Frame(tab)
        ctrl_box.pack(fill=tk.X, pady=4)
        self._btn_stream = ttk.Button(ctrl_box, text='Stream to Robot', style='Success.TButton', command=self._on_start_stream)
        self._btn_stream.pack(side=tk.LEFT, padx=3)

        self._btn_pause = ttk.Button(ctrl_box, text='Pause', command=self._on_pause_stream, state=tk.DISABLED)
        self._btn_pause.pack(side=tk.LEFT, padx=3)

        self._btn_stop = ttk.Button(ctrl_box, text='Stop / E-STOP', style='Danger.TButton', command=self._service.stop_streaming)
        self._btn_stop.pack(side=tk.LEFT, padx=3)

        self._progress_var = tk.DoubleVar(value=0.0)
        self._progress_bar = ttk.Progressbar(tab, variable=self._progress_var, maximum=100.0)
        self._progress_bar.pack(fill=tk.X, pady=3)

        self._lbl_stream_status = ttk.Label(tab, text='Streamer: Disconnected', font=('DejaVu Sans', 9, 'bold'))
        self._lbl_stream_status.pack(anchor='w')

        self._txt_log = tk.Text(tab, height=5, bg='#14161a', fg='#abb2bf', font=('DejaVu Sans Mono', 8), wrap='none')
        self._txt_log.pack(fill=tk.BOTH, expand=True, pady=2)

    def _build_validation_tab(self) -> None:
        '''
            Constructs plan validation review tab.

            :exceptions: None.
        '''
        tab: ttk.Frame = ttk.Frame(self._notebook, padding=6)
        self._notebook.add(tab, text=' Plan Validation ')

        top: ttk.Frame = ttk.Frame(tab)
        top.pack(fill=tk.X, pady=2)
        ttk.Button(top, text='Run Full Plan Validation', style='Accent.TButton', command=self._on_run_validation).pack(side=tk.LEFT)

        self._txt_val = tk.Text(tab, height=6, bg='#14161a', fg='#abb2bf', font=('DejaVu Sans Mono', 8), wrap='word')
        self._txt_val.pack(fill=tk.BOTH, expand=True, pady=4)

    def _build_jog_tab(self) -> None:
        '''
            Constructs manual Jog and auxiliary actuator panel.

            :exceptions: None.
        '''
        tab: ttk.Frame = ttk.Frame(self._notebook, padding=6)
        self._notebook.add(tab, text=' Manual Jog ')

        pwr_f: ttk.Frame = ttk.Frame(tab)
        pwr_f.pack(fill=tk.X, pady=2)
        ttk.Button(
            pwr_f,
            text='⚡ Enable Robot',
            style='Success.TButton',
            command=lambda: self._service.get_streamer().send_raw_command('<CMD:ENABLE>')
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            pwr_f,
            text='🛑 E-STOP',
            style='Danger.TButton',
            command=lambda: self._service.get_streamer().send_raw_command('<CMD:ESTOP>')
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            pwr_f,
            text='🔍 Status',
            command=lambda: self._service.get_streamer().send_raw_command('<CMD:STATUS>')
        ).pack(side=tk.LEFT, padx=2)

        step_strip: ttk.Frame = ttk.Frame(tab)
        step_strip.pack(fill=tk.X, pady=3)
        ttk.Label(step_strip, text='Step Size:').pack(side=tk.LEFT, padx=(0, 4))
        for step in (1.0, 5.0, 10.0, 25.0, 50.0):
            lbl = f'{int(step)}mm'
            ttk.Radiobutton(step_strip, text=lbl, value=step, variable=self._step_var).pack(side=tk.LEFT, padx=2)

        grid_f: ttk.Frame = ttk.Frame(tab)
        grid_f.pack(fill=tk.X, pady=3)
        ttk.Button(grid_f, text='▲ Y+', width=6, command=lambda: self._on_jog_step('Y', 1.0)).grid(row=0, column=1, padx=2, pady=2)
        ttk.Button(grid_f, text='◀ X-', width=6, command=lambda: self._on_jog_step('X', -1.0)).grid(row=1, column=0, padx=2, pady=2)
        ttk.Button(
            grid_f,
            text='Home',
            width=6,
            style='Accent.TButton',
            command=lambda: self._service.get_streamer().send_raw_command('<CMD:HOME>')
        ).grid(row=1, column=1, padx=2, pady=2)
        ttk.Button(grid_f, text='▶ X+', width=6, command=lambda: self._on_jog_step('X', 1.0)).grid(row=1, column=2, padx=2, pady=2)
        ttk.Button(grid_f, text='▼ Y-', width=6, command=lambda: self._on_jog_step('Y', -1.0)).grid(row=2, column=1, padx=2, pady=2)

        z_phi_f: ttk.Frame = ttk.Frame(tab)
        z_phi_f.pack(fill=tk.X, pady=2)
        ttk.Button(z_phi_f, text='Z+ (Up)', width=7, command=lambda: self._on_jog_step('Z', 1.0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(z_phi_f, text='Z- (Down)', width=7, command=lambda: self._on_jog_step('Z', -1.0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(z_phi_f, text='Phi+ ↺', width=7, command=lambda: self._on_jog_step('Phi', 1.0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(z_phi_f, text='Phi- ↻', width=7, command=lambda: self._on_jog_step('Phi', -1.0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            z_phi_f,
            text='Park',
            width=5,
            command=lambda: self._service.get_streamer().send_raw_command('<CMD:PARK>')
        ).pack(side=tk.LEFT, padx=2)

        aux: ttk.Frame = ttk.Frame(tab)
        aux.pack(fill=tk.X, pady=2)
        ttk.Button(
            aux,
            text='Pen UP (Z=30)',
            command=lambda: self._service.get_streamer().send_raw_command('<pt#150#0#30#40#end>')
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            aux,
            text='Pen DOWN (Z=0)',
            command=lambda: self._service.get_streamer().send_raw_command('<pt#150#0#0#40#end>')
        ).pack(side=tk.LEFT, padx=2)

        raw_f: ttk.Frame = ttk.Frame(tab)
        raw_f.pack(fill=tk.X, pady=3)
        ttk.Label(raw_f, text='CMD:').pack(side=tk.LEFT)
        self._entry_raw = ttk.Entry(raw_f, width=18)
        self._entry_raw.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)
        self._entry_raw.bind('<Return>', lambda e: self._on_send_raw())
        ttk.Button(raw_f, text='Send', width=5, style='Accent.TButton', command=self._on_send_raw).pack(side=tk.LEFT)

    def _build_preview_tab(self) -> None:
        '''
            Constructs ASCII instruction stream preview tab.

            :exceptions: None.
        '''
        tab: ttk.Frame = ttk.Frame(self._notebook, padding=6)
        self._notebook.add(tab, text=' Program Preview ')

        top: ttk.Frame = ttk.Frame(tab)
        top.pack(fill=tk.X, pady=2)
        ttk.Button(
            top,
            text='Refresh Program Preview',
            command=lambda: (
                self._txt_preview.delete('1.0', tk.END),
                self._txt_preview.insert(tk.END, TrajectoryMetrics.to_ascii_program(self._service.get_plan().waypoints))
            )
        ).pack(side=tk.LEFT)

        self._txt_preview = tk.Text(tab, height=6, bg='#14161a', fg='#abb2bf', font=('DejaVu Sans Mono', 8), wrap='none')
        self._txt_preview.pack(fill=tk.BOTH, expand=True, pady=4)

    def refresh_ports(self) -> None:
        '''
            Updates available serial ports list with USB devices prioritized.

            :exceptions: None.
        '''
        raw_ports = [p.device for p in serial.tools.list_ports.comports()]
        for p in glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyUSB*'):
            if p not in raw_ports:
                raw_ports.append(p)

        usb_ports = [p for p in raw_ports if any(tag in p for tag in ('ttyACM', 'ttyUSB', 'COM', 'cu.'))]
        other_ports = [p for p in raw_ports if p not in usb_ports and not (p.startswith('/dev/ttyS') and p[10:].isdigit())]
        dummy_ports = [p for p in raw_ports if p.startswith('/dev/ttyS') and p[10:].isdigit()]

        sorted_ports = usb_ports + other_ports + dummy_ports
        self._cbo_ports['values'] = sorted_ports

        if usb_ports:
            self._cbo_ports.set(usb_ports[0])
        elif sorted_ports and not self._cbo_ports.get():
            self._cbo_ports.set(sorted_ports[0])

    def append_log(self, text: str, is_outgoing: bool = False) -> None:
        '''
            Appends message to terminal log console.

            :param text: Message string.
            :param is_outgoing: Flag indicating outgoing transmission.
            :exceptions: None.
        '''
        prefix: str = '>>> ' if is_outgoing else '<<< '
        self._txt_log.insert(tk.END, f'{prefix}{text}\n')
        self._txt_log.see(tk.END)

    def update_progress(self, progress: StreamProgress) -> None:
        '''
            Updates streamer progress bar and metrics.

            :param progress: StreamProgress metric container.
            :exceptions: None.
        '''
        self._progress_var.set(progress.percentage)
        st_name: str = progress.state.name
        self._lbl_stream_status.configure(
            text=f'Streamer: {st_name} | Sent: {progress.sent_waypoints}/{progress.total_waypoints} | '
            f'Done: {progress.completed_waypoints} | Time: {progress.elapsed_seconds:.1f}s'
        )

        match progress.state:
            case StreamState.STREAMING:
                self._btn_stream.configure(state=tk.DISABLED)
                self._btn_pause.configure(state=tk.NORMAL, text='Pause')
            case StreamState.PAUSED:
                self._btn_pause.configure(state=tk.NORMAL, text='Resume')
            case _:
                self._btn_stream.configure(state=tk.NORMAL)
                self._btn_pause.configure(state=tk.DISABLED)

    def _on_toggle_connect(self) -> None:
        '''
            Connects or disconnects serial port.

            :exceptions: None.
        '''
        streamer = self._service.get_streamer()
        if streamer.is_connected():
            streamer.disconnect()
            self._btn_connect.configure(text='Connect', style='Accent.TButton')
            self._lbl_stream_status.configure(text='Streamer: Disconnected')
        else:
            port: str = self._cbo_ports.get()
            if not port:
                messagebox.showerror('Serial Port Error', 'No serial port selected.')
                return
            config: StreamConfigDTO = StreamConfigDTO(port=port, baudrate=115200, timeout=0.1)
            if streamer.connect_with_config(config):
                self._btn_connect.configure(text='Disconnect', style='Danger.TButton')
                self._lbl_stream_status.configure(text=f'Streamer: Connected to {port}')

    def _on_start_stream(self) -> None:
        '''
            Starts streaming trajectory after validation check.

            :exceptions: None.
        '''
        valid, msgs = self._service.validate_plan()
        if not valid:
            res: bool = messagebox.askyesno(
                'Validation Warnings',
                'Plan has validation warnings/errors:\n\n' + '\n'.join(msgs[:4]) + '\n\nDo you want to proceed anyway?'
            )
            if not res:
                return

        if not self._service.start_streaming():
            messagebox.showerror('Stream Error', 'Failed to start stream. Check serial connection.')

    def _on_pause_stream(self) -> None:
        '''
            Toggles stream pause/resume.

            :exceptions: None.
        '''
        streamer = self._service.get_streamer()
        if self._btn_pause.cget('text') == 'Pause':
            streamer.pause_streaming()
        else:
            streamer.resume_streaming()

    def _on_run_validation(self) -> None:
        '''
            Runs and displays validation report.

            :exceptions: None.
        '''
        valid, msgs = self._service.validate_plan()
        self._txt_val.delete('1.0', tk.END)
        for msg in msgs:
            prefix: str = '✅ ' if 'PASSED' in msg else '❌ '
            self._txt_val.insert(tk.END, f'{prefix}{msg}\n')

    def _on_jog_step(self, axis: str, sign: float = 1.0) -> None:
        '''
            Sends relative jog command based on selected step size.

            :param axis: Axis identifier ('X', 'Y', 'Z', 'Phi').
            :param sign: Direction multiplier (+1.0 or -1.0).
            :exceptions: None.
        '''
        delta: float = self._step_var.get() * sign
        cmd: str = f'<CMD:JOG#{axis}#{delta:.1f}>'
        streamer = self._service.get_streamer()
        streamer.send_raw_command(cmd)
        streamer.send_raw_command('<CMD:STATUS>')

    def _on_send_raw(self) -> None:
        '''
            Transmits raw command from text input to microcontroller.

            :exceptions: None.
        '''
        cmd: str = self._entry_raw.get().strip()
        if cmd:
            self._service.get_streamer().send_raw_command(cmd)
            self._entry_raw.delete(0, tk.END)
