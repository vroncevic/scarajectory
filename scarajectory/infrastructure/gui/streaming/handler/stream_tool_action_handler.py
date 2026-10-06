# -*- coding: UTF-8 -*-

'''
Module
    stream_tool_action_handler.py
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
    Action handler coordinating manipulator tooling, homing calibration, and feedrate overrides.
'''

from __future__ import annotations

from tkinter.messagebox import showinfo
from typing import Final

from scarajectory.infrastructure.connection.istream_connection import IStreamConnection
from scarajectory.core.service.manipulator.ijog_controller import IJogController
from scarajectory.core.service.manipulator.imotion_controller import IMotionController
from scarajectory.core.service.tool.itool_controller import IToolController
from scarajectory.infrastructure.gui.manipulator.imanipulator_override_panel import IManipulatorOverridePanel
from scarajectory.infrastructure.gui.streaming.streamer_controllers_bundle import StreamerControllersBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamToolActionHandler:
    '''
        Action handler coordinating manipulator tooling, homing calibration, and feedrate overrides.

        It defines:

            :attributes:
                | _connection - Stream transport connection controller.
                | _motion_controller - Motion controller interface.
                | _jog_controller - Jog and speed override controller interface.
                | _tool_controller - Tool actuation controller interface.
                | _override_panel - Manipulator override panel protocol.
                | _pump_state - Flag storing end-effector vacuum pump active state.
            :methods:
                | __init__ - Initializes tool action handler with collaborators.
                | on_home_robot - Transmits homing calibration command.
                | on_toggle_pump - Toggles vacuum pump state.
                | on_purge_valve - Sends momentary purge valve pulse command.
                | on_override_change - Updates feedrate speed override percentage.
    '''

    _connection: IStreamConnection
    _motion_controller: IMotionController
    _jog_controller: IJogController
    _tool_controller: IToolController
    _override_panel: IManipulatorOverridePanel
    _pump_state: bool

    def __init__(
        self,
        *,
        connection: IStreamConnection,
        controllers: StreamerControllersBundle,
        override_panel: IManipulatorOverridePanel,
    ) -> None:
        '''
            Initializes tool action handler with hardware collaborators.

            :param connection: Injected IStreamConnection instance.
            :param controllers: Injected StreamerControllersBundle instance.
            :param override_panel: Injected IManipulatorOverridePanel instance.
            :exceptions: None.
        '''
        self._connection: Final[IStreamConnection] = connection
        self._motion_controller: Final[IMotionController] = controllers.motion_controller
        self._jog_controller: Final[IJogController] = controllers.jog_controller
        self._tool_controller: Final[IToolController] = controllers.tool_controller
        self._override_panel: Final[IManipulatorOverridePanel] = override_panel
        self._pump_state = False

    def on_home_robot(self) -> None:
        '''
            Transmits homing calibration command sequence.

            :exceptions: None.
        '''
        if not self._connection.is_connected():
            return

        self._motion_controller.home()
        showinfo('Homing', 'Homing command transmitted.')

    def on_toggle_pump(self) -> None:
        '''
            Toggles end-effector vacuum pump state and updates status indicator.

            :exceptions: None.
        '''
        if not self._connection.is_connected():
            return

        self._pump_state = not self._pump_state
        self._tool_controller.set_pump(self._pump_state)
        self._override_panel.set_pump_active(self._pump_state)

    def on_purge_valve(self) -> None:
        '''
            Sends momentary purge valve pulse command.

            :exceptions: None.
        '''
        if not self._connection.is_connected():
            return

        self._tool_controller.pulse_valve(150)

    def on_override_change(self, val: str) -> None:
        '''
            Updates feedrate speed override percentage dynamically.

            :param val: Override percentage string representation.
            :exceptions: None.
        '''
        if not self._connection.is_connected():
            return

        pct: int = int(float(val))
        self._override_panel.set_override_label(pct)
        self._jog_controller.set_speed_override(pct)
