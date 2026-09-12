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

from tkinter import BOTH, Widget, X
from tkinter.messagebox import askyesno, showerror, showinfo
from tkinter.ttk import Frame
from typing import Final

from scarajectory.core.model.communication.stream_config import StreamConfig
from scarajectory.core.model.communication.stream_progress import StreamProgress
from scarajectory.core.model.trajectory.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.service.trajectory.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.communication.irobot_controller import IRobotController
from scarajectory.core.service.communication.itrajectory_streamer import ITrajectoryStreamer
from scarajectory.core.service.iservice import IService
from scarajectory.infrastructure.gui.stream.serial_console import SerialConsole
from scarajectory.infrastructure.gui.stream.stream_status_bar import StreamStatusBar
from scarajectory.infrastructure.gui.stream.port_connection_panel import PortConnectionPanel
from scarajectory.infrastructure.gui.stream.stream_control_panel import StreamControlPanel
from scarajectory.infrastructure.gui.stream.robot_override_panel import RobotOverridePanel
from scarajectory.infrastructure.gui.stream.stream_progress_adapter import StreamProgressAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamerTab(Frame):
    '''
        Hardware connection and trajectory streaming tab orchestrating connection, controls, and diagnostics.

        It defines:

            :attributes:
                | _plan - Active trajectory plan domain abstraction.
                | _validator - Kinematic reachability validator.
                | _streamer - Robot communication and streaming service.
                | _service - Optional application facade service.
                | _port_panel - Serial port connection subpanel.
                | _ctrl_panel - Streaming control buttons subpanel.
                | _override_panel - Robot actuators and override subpanel.
                | _status_bar - Progress bar and summary readout widget.
                | _console - Serial communication terminal output component.
                | _pump_state - Flag storing end-effector vacuum pump active state.
            :methods:
                | __init__ - Initializes the streamer tab panel.
                | refresh_ports - Scans available serial/USB ports on the host.
                | append_log - Appends message to terminal log console.
                | update_progress - Updates streamer progress bar and metrics.
                | _on_toggle_connect - Connects or disconnects from selected serial port.
                | _on_start_stream - Starts streaming trajectory after validation check.
                | _on_pause_resume_stream - Toggles stream pause/resume.
                | _on_override_change - Transmits feedrate speed override command to robot.
                | _on_home_robot - Transmits homing calibration command to robot.
                | _on_toggle_pump - Toggles vacuum pump state on or off.
                | _on_purge_valve - Sends momentary purge valve command pulse.
    '''

    _plan: ITrajectoryPlan
    _validator: ITrajectoryValidator
    _streamer: ITrajectoryStreamer
    _robot_controller: IRobotController | None
    _service: IService | None
    _port_panel: PortConnectionPanel
    _ctrl_panel: StreamControlPanel
    _override_panel: RobotOverridePanel
    _status_bar: StreamStatusBar
    _console: SerialConsole
    _progress_adapter: StreamProgressAdapter
    _pump_state: bool

    def __init__(
        self,
        parent: Widget,
        plan: ITrajectoryPlan,
        validator: ITrajectoryValidator,
        streamer: ITrajectoryStreamer,
        service: IService | None = None,
        **kwargs: object,
    ) -> None:
        '''
            Initializes the streamer tab panel.

            :param parent: Parent notebook widget.
            :param plan: Active ITrajectoryPlan.
            :param validator: ITrajectoryValidator instance.
            :param streamer: ITrajectoryStreamer instance.
            :param service: Optional IService facade instance.
            :exceptions: None.
        '''
        super().__init__(parent, padding=6, **kwargs)
        self._plan: Final[ITrajectoryPlan] = plan
        self._validator: Final[ITrajectoryValidator] = validator
        self._streamer: Final[ITrajectoryStreamer] = streamer
        self._robot_controller = getattr(streamer, 'get_robot_controller', lambda: None)()
        self._service: Final[IService | None] = service
        self._pump_state = False

        self._port_panel = PortConnectionPanel(self, on_toggle_connect=self._on_toggle_connect)
        self._port_panel.pack(fill=X, pady=2)

        self._ctrl_panel = StreamControlPanel(
            self,
            on_start_stream=self._on_start_stream,
            on_pause_resume=self._on_pause_resume_stream,
            on_stop=self._streamer.stop_streaming,
        )
        self._ctrl_panel.pack(fill=X, pady=4)

        self._override_panel = RobotOverridePanel(
            self,
            on_home=self._on_home_robot,
            on_toggle_pump=self._on_toggle_pump,
            on_purge_valve=self._on_purge_valve,
            on_override_change=self._on_override_change,
        )
        self._override_panel.pack(fill=X, pady=2)

        self._status_bar = StreamStatusBar(self)
        self._status_bar.pack(fill=X, pady=2)

        self._progress_adapter = StreamProgressAdapter(
            port_panel=self._port_panel,
            status_bar=self._status_bar,
        )

        self._console = SerialConsole(self)
        self._console.pack(fill=BOTH, expand=True, pady=2)

    def refresh_ports(self) -> None:
        '''
            Scans and lists active serial / tty ports on the host system.

            :exceptions: None.
        '''
        self._port_panel.refresh_ports()

    def append_log(self, text: str, is_outgoing: bool = False) -> None:
        '''
            Appends timestamped message to the terminal console widget.

            :param text: Message string.
            :param is_outgoing: True if transmitted command.
            :exceptions: None.
        '''
        self._console.append_log(text, is_outgoing)
        self._progress_adapter.handle_log_message(text)

    def update_progress(self, progress: StreamProgress) -> None:
        '''
            Updates progress bar and streaming status indicator widgets.

            :param progress: StreamProgress data model.
            :exceptions: None.
        '''
        self._progress_adapter.update_progress(progress)

    def _on_toggle_connect(self) -> None:
        '''
            Connects or disconnects from selected serial port.

            :exceptions: None.
        '''
        if self._streamer.is_connected():
            self._streamer.disconnect()
            self._progress_adapter.set_disconnected()
        else:
            port: str = self._port_panel.get_selected_port()
            if not port:
                showerror('Serial Port Error', 'No serial port selected.')
                return

            config: StreamConfig = StreamConfig(port=port, baudrate=115200, timeout=0.1)
            if self._streamer.connect_with_config(config):
                self._progress_adapter.set_connected(port)

    def _on_start_stream(self) -> None:
        '''
            Starts streaming trajectory after validation check.

            :exceptions: None.
        '''
        if self._service is not None:
            valid, msgs = self._service.validate_plan()
        else:
            valid, msgs = self._validator.validate_plan(self._plan)

        if not valid:
            res: bool = askyesno(
                'Validation Warnings',
                'Plan has validation warnings/errors:\n\n' + '\n'.join(msgs[:4]) + '\n\nDo you want to proceed anyway?'
            )
            if not res:
                return

        started: bool = self._streamer.start_streaming(self._plan.waypoints)
        if not started:
            showerror('Stream Error', 'Failed to start stream. Check serial connection.')

    def _on_pause_resume_stream(self) -> None:
        '''
            Toggles stream pause/resume.

            :exceptions: None.
        '''
        try:
            self._streamer.pause_streaming()
        except (AttributeError, RuntimeError):
            self._streamer.resume_streaming()

    def _on_override_change(self, pct: int) -> None:
        '''
            Transmits feedrate speed override command to robot.

            :param pct: Percentage speed integer.
            :exceptions: None.
        '''
        if self._streamer.is_connected() and self._robot_controller is not None:
            self._robot_controller.set_feedrate_override(pct)

    def _on_home_robot(self) -> None:
        '''
            Transmits homing calibration command to robot.

            :exceptions: None.
        '''
        if self._streamer.is_connected() and self._robot_controller is not None:
            self._robot_controller.home()
        else:
            showinfo('Hardware Offline', 'Connect to robot first to run homing.')

    def _on_toggle_pump(self) -> None:
        '''
            Toggles vacuum pump state on or off.

            :exceptions: None.
        '''
        if self._streamer.is_connected() and self._robot_controller is not None:
            self._pump_state = not self._pump_state
            self._override_panel.set_pump_state(self._pump_state)
            self._robot_controller.set_vacuum_pump(self._pump_state)
        else:
            showinfo('Hardware Offline', 'Connect to robot first.')

    def _on_purge_valve(self) -> None:
        '''
            Sends momentary purge valve command pulse.

            :exceptions: None.
        '''
        if self._streamer.is_connected() and self._robot_controller is not None:
            self._robot_controller.pulse_purge_valve()
        else:
            showinfo('Hardware Offline', 'Connect to robot first.')
