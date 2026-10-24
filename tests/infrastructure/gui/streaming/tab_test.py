# -*- coding: UTF-8 -*-

'''
Module
    tab_test.py
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

from scarajectory.core.model.streaming.state import StreamState
from scarajectory.core.model.telemetry.counts import ProgressCounts
from scarajectory.core.model.telemetry.progress import StreamProgress
from scarajectory.infrastructure.gui.streaming.tab import StreamerTab

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
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
                | test_initialization - Tests tab frame instantiation.
                | test_bind_and_delegation - Tests component binding and event delegation.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        '''
            Sets up test class fixture.

            :exceptions: None.
        '''
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        '''
            Tears down test class fixture.

            :exceptions: None.
        '''
        cls.root.destroy()

    def test_initialization(self) -> None:
        '''
            Verifies StreamerTab frame construction.

            :exceptions: None.
        '''
        tab: StreamerTab = StreamerTab(self.root)
        self.assertIsInstance(tab, StreamerTab)
        tab.destroy()

    def test_bind_and_delegation(self) -> None:
        '''
            Verifies component binding and execution of logs and progress updates.

            :exceptions: None.
        '''
        tab: StreamerTab = StreamerTab(self.root)

        mock_port_panel: MagicMock = MagicMock()
        mock_progress_adapter: MagicMock = MagicMock()
        mock_console: MagicMock = MagicMock()

        tab.bind_components(
            port_panel=mock_port_panel,
            progress_adapter=mock_progress_adapter,
            console=mock_console,
        )

        tab.refresh_ports()
        mock_port_panel.refresh_ports.assert_called_once()

        tab.append_log('G1 X100 Y50', is_outgoing=True)
        mock_console.append_log.assert_called_once_with('G1 X100 Y50', True)
        mock_progress_adapter.handle_log_message.assert_called_once_with('G1 X100 Y50')

        progress: StreamProgress = StreamProgress(
            state=StreamState.STREAMING,
            counts=ProgressCounts(
                total=5,
                sent=2,
                completed=1,
                failed=0,
            ),
            current_line='G1 X100 Y50',
            error_message='',
            elapsed_seconds=0.5,
            percentage=20.0,
        )
        tab.update_progress(progress)
        mock_progress_adapter.update_progress.assert_called_once_with(progress)

        tab.destroy()


if __name__ == '__main__':
    main()
