# -*- coding: UTF-8 -*-

'''
Module
    streamer_tab_test.py
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
    Unit testing for StreamerTab component.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.preferences.connection_preference import (
    ConnectionPreference,
)
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.telemetry.stream_progress import StreamProgress
from scarajectory.infrastructure.gui.connection.port_connection_panel import (
    PortConnectionPanel,
)
from scarajectory.infrastructure.gui.console.serial_console import (
    SerialConsole,
)
from scarajectory.infrastructure.gui.manipulator.manipulator_override_panel import (
    ManipulatorOverridePanel,
)
from scarajectory.infrastructure.gui.streaming.panel.stream_progress_adapter import (
    StreamProgressAdapter,
)
from scarajectory.infrastructure.gui.streaming.panel.stream_status_bar import (
    StreamStatusBar,
)
from scarajectory.infrastructure.gui.streaming.streamer_action_bundle import (
    StreamerActionBundle,
)
from scarajectory.infrastructure.gui.streaming.streamer_tab import (
    StreamerTab,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamerTabTestCase(TestCase):
    '''
        Unit tests for StreamerTab component.

        It defines:

            :methods:
                | setUpClass - Initializes root Tk instance.
                | tearDownClass - Destroys root Tk instance.
                | test_initialization_and_subpanels - Tests subpanel creation and properties.
                | test_mount_actions_and_delegation - Tests mounting actions and event flow.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.root.destroy()

    def test_initialization_and_subpanels(self) -> None:
        '''Verifies StreamerTab construction and subpanel property exposure.'''
        mock_repo = MagicMock()
        mock_repo.load_preference.return_value = ConnectionPreference(
            port='/dev/ttyUSB0', baud=115200
        )
        tab = StreamerTab(self.root, connection_repository=mock_repo)

        self.assertIsInstance(tab.port_panel, PortConnectionPanel)
        self.assertIsInstance(tab.status_bar, StreamStatusBar)
        self.assertIsInstance(tab.progress_adapter, StreamProgressAdapter)
        self.assertIsInstance(tab.override_panel, ManipulatorOverridePanel)
        tab.destroy()

    def test_mount_actions_and_delegation(self) -> None:
        '''Verifies action mounting and execution of logs and progress updates.'''
        mock_repo = MagicMock()
        mock_repo.load_preference.return_value = ConnectionPreference(
            port='/dev/ttyUSB0', baud=115200
        )
        tab = StreamerTab(self.root, connection_repository=mock_repo)

        mock_playback = MagicMock()
        mock_tool = MagicMock()
        actions = StreamerActionBundle(
            playback_handler=mock_playback,
            tool_handler=mock_tool,
        )
        tab.mount_actions(actions)

        self.assertIs(tab.actions, actions)
        self.assertIsInstance(tab.console, SerialConsole)

        tab.refresh_ports()
        tab.append_log('G1 X100 Y50', is_outgoing=True)

        progress = StreamProgress(
            state=StreamState.STREAMING,
            total_waypoints=5,
            sent_waypoints=2,
            completed_waypoints=1,
            failed_waypoints=0,
            current_line='G1 X100 Y50',
            error_message='',
            elapsed_seconds=0.5,
            percentage=20.0,
        )
        tab.update_progress(progress)
        tab.destroy()


if __name__ == '__main__':
    main()
