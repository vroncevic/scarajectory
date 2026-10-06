# -*- coding: UTF-8 -*-

'''
Module
    stream_progress_adapter_test.py
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
    Unit tests for StreamProgressAdapter connection and metrics synchronizer.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.telemetry.stream_progress import StreamProgress
from scarajectory.infrastructure.gui.streaming.panel.stream_progress_adapter import StreamProgressAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StubPortConnectionPanel:
    '''
        Structural stub for port connection control panel.
    '''

    def __init__(self) -> None:
        self.connected_state: bool | None = None

    def set_connected_state(self, state: bool) -> None:
        '''Updates port connection indicator.'''
        self.connected_state = state

    def is_connected(self) -> bool:
        '''Returns current connected state.'''
        return bool(self.connected_state)

    def get_selected_port(self) -> str:
        '''Returns currently selected port.'''
        return '/dev/ttyUSB0'


class StubStreamStatusBar:
    '''
        Structural stub for streaming status bar.
    '''

    def __init__(self) -> None:
        self.last_progress: StreamProgress | None = None
        self.status_text: str = ''

    def update_progress(self, progress: StreamProgress) -> None:
        '''Updates progress data model.'''
        self.last_progress = progress

    def set_status_text(self, text: str) -> None:
        '''Updates status bar message.'''
        self.status_text = text


class StreamProgressAdapterTestCase(TestCase):
    '''
        Tests for StreamProgressAdapter connection and metrics synchronization.

        It defines:

            :methods:
                | test_update_progress - Verifies progress model is forwarded to status bar.
                | test_handle_log_message_disconnection - Verifies disconnect on connection loss.
                | test_handle_log_message_connection - Verifies connect on connection message.
                | test_handle_log_message_ignored - Verifies prompt output is ignored.
                | test_direct_connection_controls - Verifies set_connected and set_disconnected.
    '''

    def test_update_progress(self) -> None:
        '''
            Verifies progress model is forwarded to status bar.

            :exceptions: None.
        '''
        port_panel = StubPortConnectionPanel()
        status_bar = StubStreamStatusBar()
        adapter = StreamProgressAdapter(port_panel, status_bar)

        progress = StreamProgress(
            state=StreamState.STREAMING,
            total_waypoints=100,
            sent_waypoints=50,
            completed_waypoints=48,
            failed_waypoints=0,
            current_line='G1 X20 Y30',
            error_message='',
            elapsed_seconds=5.0,
            percentage=50.0,
        )
        adapter.update_progress(progress)
        self.assertEqual(status_bar.last_progress, progress)

    def test_handle_log_message_disconnection(self) -> None:
        '''
            Verifies disconnect detection on connection lost or disconnected from.

            :exceptions: None.
        '''
        port_panel = StubPortConnectionPanel()
        status_bar = StubStreamStatusBar()
        adapter = StreamProgressAdapter(port_panel, status_bar)

        adapter.handle_log_message('Error: Connection lost unexpectedly')
        self.assertFalse(port_panel.connected_state)
        self.assertEqual(status_bar.status_text, 'Streamer: Disconnected')

        adapter.handle_log_message('Disconnected from /dev/ttyUSB0')
        self.assertFalse(port_panel.connected_state)
        self.assertEqual(status_bar.status_text, 'Streamer: Disconnected')

    def test_handle_log_message_connection(self) -> None:
        '''
            Verifies connect detection when message contains connected target.

            :exceptions: None.
        '''
        port_panel = StubPortConnectionPanel()
        status_bar = StubStreamStatusBar()
        adapter = StreamProgressAdapter(port_panel, status_bar)

        adapter.handle_log_message('Connected to /dev/ttyUSB1 with 115200 baud')
        self.assertTrue(port_panel.connected_state)
        self.assertEqual(
            status_bar.status_text,
            'Streamer: Connected to /dev/ttyUSB1',
        )

    def test_handle_log_message_ignored(self) -> None:
        '''
            Verifies console prompt outputs starting with >>> are ignored.

            :exceptions: None.
        '''
        port_panel = StubPortConnectionPanel()
        status_bar = StubStreamStatusBar()
        adapter = StreamProgressAdapter(port_panel, status_bar)

        adapter.handle_log_message('>>> Connected to /dev/ttyUSB0')
        self.assertIsNone(port_panel.connected_state)
        self.assertEqual(status_bar.status_text, '')

    def test_direct_connection_controls(self) -> None:
        '''
            Verifies direct calls to set_connected and set_disconnected.

            :exceptions: None.
        '''
        port_panel = StubPortConnectionPanel()
        status_bar = StubStreamStatusBar()
        adapter = StreamProgressAdapter(port_panel, status_bar)

        adapter.set_connected('/dev/ttyACM0')
        self.assertTrue(port_panel.connected_state)
        self.assertEqual(
            status_bar.status_text,
            'Streamer: Connected to /dev/ttyACM0',
        )

        adapter.set_disconnected()
        self.assertFalse(port_panel.connected_state)
        self.assertEqual(status_bar.status_text, 'Streamer: Disconnected')


if __name__ == '__main__':
    main()
