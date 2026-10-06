# -*- coding: UTF-8 -*-

'''
Module
    stream_playback_action_handler_test.py
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
    Unit testing for StreamPlaybackActionHandler component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.streaming.handler.playback_handler_bundle import PlaybackHandlerBundle
from scarajectory.infrastructure.gui.streaming.handler.stream_playback_action_handler import StreamPlaybackActionHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStreamPlaybackActionHandler(TestCase):
    '''
        Test cases verifying StreamPlaybackActionHandler functionality.

        It defines:

            :methods:
                | setUp - Initializes mock collaborators and handler instance.
                | test_toggle_connection - Tests connect, disconnect, and empty port handling.
                | test_on_start_stream - Tests starting stream under valid and warning flows.
                | test_on_pause_resume_stream - Tests pause and exception fallback to resume.
                | test_on_stop_stream - Tests aborting active stream transmission.
    '''

    def setUp(self) -> None:
        '''Initializes mock collaborators and action handler under test.'''
        self.mock_plan = MagicMock()
        self.mock_plan.waypoints = []
        self.mock_validator = MagicMock()
        self.mock_validator.validate_plan.return_value = (True, [])
        self.mock_streamer = MagicMock()
        self.mock_progress_adapter = MagicMock()
        self.mock_port_panel = MagicMock()
        self.mock_port_panel.get_selected_port.return_value = '/dev/ttyUSB0'

        bundle = PlaybackHandlerBundle(
            plan=self.mock_plan,
            validator=self.mock_validator,
            connection=self.mock_streamer,
            playback_controller=self.mock_streamer,
            progress_adapter=self.mock_progress_adapter,
            port_panel=self.mock_port_panel,
        )
        self.handler = StreamPlaybackActionHandler(bundle=bundle)

    @patch(
        'scarajectory.infrastructure.gui.streaming.handler.'
        'stream_playback_action_handler.showerror'
    )
    def test_toggle_connection(self, mock_showerror: MagicMock) -> None:
        '''Tests disconnecting, connecting, failed connect, and empty port handling.'''
        self.mock_streamer.is_connected.return_value = True
        self.handler.toggle_connection()
        self.mock_streamer.disconnect.assert_called_once()
        self.mock_progress_adapter.set_disconnected.assert_called_once()

        self.mock_streamer.is_connected.return_value = False
        self.mock_streamer.connect_with_config.return_value = True
        self.handler.toggle_connection()
        self.mock_streamer.connect_with_config.assert_called_once()
        self.mock_progress_adapter.set_connected.assert_called_once_with(
            '/dev/ttyUSB0'
        )

        self.mock_streamer.connect_with_config.return_value = False
        self.handler.toggle_connection()

        self.mock_port_panel.get_selected_port.return_value = ''
        self.handler.toggle_connection()
        mock_showerror.assert_called_once_with(
            'Serial Port Error', 'No serial port selected.'
        )

    @patch(
        'scarajectory.infrastructure.gui.streaming.handler.'
        'stream_playback_action_handler.showerror'
    )
    @patch(
        'scarajectory.infrastructure.gui.streaming.handler.'
        'stream_playback_action_handler.askyesno'
    )
    def test_on_start_stream(
        self, mock_askyesno: MagicMock, mock_showerror: MagicMock
    ) -> None:
        '''Tests stream start with valid plan, rejected warnings, and start errors.'''
        self.mock_streamer.start_streaming.return_value = True
        self.handler.on_start_stream()
        self.mock_streamer.start_streaming.assert_called_once_with([])

        self.mock_validator.validate_plan.return_value = (
            False, ['W1', 'W2', 'W3', 'W4', 'W5']
        )
        mock_askyesno.return_value = False
        self.handler.on_start_stream()

        mock_askyesno.return_value = True
        self.mock_streamer.start_streaming.return_value = False
        self.handler.on_start_stream()
        mock_showerror.assert_called_once_with(
            'Stream Error', 'Failed to start stream. Check serial connection.'
        )

    def test_on_pause_resume_stream(self) -> None:
        '''Tests toggling pause and catching exception to resume.'''
        self.handler.on_pause_resume_stream()
        self.mock_streamer.pause_streaming.assert_called_once()

        self.mock_streamer.pause_streaming.side_effect = RuntimeError(
            'Cannot pause'
        )
        self.handler.on_pause_resume_stream()
        self.mock_streamer.resume_streaming.assert_called_once()

    def test_on_stop_stream(self) -> None:
        '''Tests aborting and stopping active stream transmission.'''
        self.handler.on_stop_stream()
        self.mock_streamer.stop_streaming.assert_called_once()


if __name__ == '__main__':
    main()
