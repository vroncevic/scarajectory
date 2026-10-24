# -*- coding: UTF-8 -*-

'''
Module
    handler_test.py
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

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.gui.streaming.playback.bundle import PlaybackHandlerBundle
from scarajectory.infrastructure.gui.streaming.playback.handler import StreamPlaybackActionHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlaybackMocksHolder:
    '''
        Mock collaborators container for TestStreamPlaybackActionHandler.

        It defines:

            :attributes:
                | plan - Mock waypoint query plan.
                | validator - Mock trajectory validator.
                | avoidance - Mock avoidance adapter.
                | conn - Mock connection manager.
                | playback - Mock playback controller.
                | status_bar - Mock status bar protocol.
            :methods:
                | __init__ - Initializes mock collaborators.
                | build_bundle - Assembles PlaybackHandlerBundle from mocks.
                | reset_mocks - Resets mock invocation states.
    '''

    def __init__(self) -> None:
        '''
            Initializes mock collaborators.

            :exceptions: None.
        '''
        self.plan: MagicMock = MagicMock()
        self.plan.waypoints = []
        self.validator: MagicMock = MagicMock()
        self.validator.validate_plan.return_value = (True, [])
        self.avoidance: MagicMock = MagicMock()
        self.avoidance.crosses_dead_zone.return_value = False
        self.conn: MagicMock = MagicMock()
        self.playback: MagicMock = MagicMock()
        self.status_bar: MagicMock = MagicMock()

    def build_bundle(self) -> PlaybackHandlerBundle:
        '''
            Assembles PlaybackHandlerBundle from mocks.

            :return: Configured PlaybackHandlerBundle instance.
            :exceptions: None.
        '''
        return PlaybackHandlerBundle(
            plan=self.plan,
            validator=self.validator,
            avoidance_adapter=self.avoidance,
            connection_manager=self.conn,
            playback_controller=self.playback,
            status_bar=self.status_bar,
        )

    def reset_mocks(self) -> None:
        '''
            Resets mock invocation states.

            :exceptions: None.
        '''
        self.plan.reset_mock()
        self.validator.reset_mock()


class TestStreamPlaybackActionHandler(TestCase):
    '''
        Test cases verifying StreamPlaybackActionHandler functionality.

        It defines:

            :methods:
                | setUp - Initializes mock collaborators and handler instance.
                | test_toggle_connection - Tests connect, disconnect, and empty port handling.
                | test_is_connected - Verifies is_connected delegates to connection manager.
                | test_on_start_stream - Tests starting stream under valid and warning flows.
                | test_on_start_stream_with_dead_zone_lead_in - Tests detour prepending for dead zone transit.
                | test_on_pause_resume_stream - Tests pause and exception fallback to resume.
                | test_on_stop_stream - Tests aborting active stream transmission.
    '''

    def setUp(self) -> None:
        '''
            Initializes mock collaborators and action handler under test.

            :exceptions: None.
        '''
        self.mocks = PlaybackMocksHolder()
        self.handler = StreamPlaybackActionHandler(
            bundle=self.mocks.build_bundle()
        )

    @patch('scarajectory.infrastructure.gui.streaming.playback.handler.showerror')
    def test_toggle_connection(self, mock_showerror: MagicMock) -> None:
        '''
            Tests disconnecting, connecting, failed connect, and empty port handling.

            :param mock_showerror: Mocked showerror dialog function.
            :exceptions: None.
        '''
        mock_conn = self.mocks.conn
        mock_status = self.mocks.status_bar

        mock_conn.is_connected.return_value = True
        self.handler.toggle_connection('/dev/ttyUSB0')
        mock_conn.disconnect.assert_called_once()
        mock_status.set_status_text.assert_called_once_with('Streamer: Disconnected')

        mock_conn.is_connected.return_value = False
        mock_conn.connect_with_config.return_value = True
        self.handler.toggle_connection('/dev/ttyUSB0')
        mock_conn.connect_with_config.assert_called_once()
        mock_status.set_status_text.assert_called_with('Streamer: Connected to /dev/ttyUSB0')

        mock_conn.connect_with_config.return_value = False
        self.handler.toggle_connection('/dev/ttyUSB0')

        self.handler.toggle_connection('')
        mock_showerror.assert_called_with(
            'Serial Port Error', 'No serial port selected.'
        )

    def test_is_connected(self) -> None:
        '''
            Verifies is_connected delegates to connection manager.

            :exceptions: None.
        '''
        mock_conn = self.mocks.conn
        mock_conn.is_connected.return_value = True
        self.assertTrue(self.handler.is_connected())
        mock_conn.is_connected.return_value = False
        self.assertFalse(self.handler.is_connected())

    @patch('scarajectory.infrastructure.gui.streaming.playback.handler.showerror')
    @patch('scarajectory.infrastructure.gui.streaming.playback.handler.askyesno')
    def test_on_start_stream(
        self, mock_askyesno: MagicMock, mock_showerror: MagicMock
    ) -> None:
        '''
            Tests stream start with valid plan, rejected warnings, and start errors.

            :param mock_askyesno: Mocked askyesno dialog function.
            :param mock_showerror: Mocked showerror dialog function.
            :exceptions: None.
        '''
        mock_playback = self.mocks.playback
        mock_validator = self.mocks.validator
        mock_plan = self.mocks.plan

        mock_playback.start_streaming.return_value = True
        self.handler.on_start_stream()
        mock_playback.start_streaming.assert_called_once_with([])

        wp1 = TrajectoryWaypoint(x=150.0, y=0.0, z=20.0, speed=50.0, phi=0.0, name='', command='')
        wp2 = TrajectoryWaypoint(x=160.0, y=10.0, z=20.0, speed=50.0, phi=0.0, name='', command='')
        mock_plan.waypoints = [wp1, wp2]
        self.mocks.avoidance.crosses_dead_zone.return_value = False
        self.handler.on_start_stream()
        mock_playback.start_streaming.assert_called_with([wp1, wp2])

        mock_plan.waypoints = []
        mock_validator.validate_plan.return_value = (
            False, ['W1', 'W2', 'W3', 'W4', 'W5']
        )
        mock_askyesno.return_value = False
        self.handler.on_start_stream()

        mock_askyesno.return_value = True
        mock_playback.start_streaming.return_value = False
        self.handler.on_start_stream()
        mock_showerror.assert_called_with(
            'Stream Error', 'Failed to start stream. Check serial connection.'
        )

    def test_on_start_stream_with_dead_zone_lead_in(self) -> None:
        '''
            Tests detour prepending for dead zone transit.

            :exceptions: None.
        '''
        mock_plan = self.mocks.plan
        mock_avoidance = self.mocks.avoidance
        mock_playback = self.mocks.playback

        target_wp = TrajectoryWaypoint(x=-125.7, y=66.0, z=20.0, speed=100.0, phi=0.0, name='', command='')
        second_wp = TrajectoryWaypoint(x=120.0, y=-50.0, z=20.0, speed=100.0, phi=0.0, name='', command='')
        mock_plan.waypoints = [target_wp, second_wp]
        mock_avoidance.crosses_dead_zone.side_effect = [True, True]
        bypass_wp = TrajectoryWaypoint(x=50.0, y=80.0, z=20.0, speed=100.0, phi=0.0, name='', command='')
        bypass_wp2 = TrajectoryWaypoint(x=80.0, y=0.0, z=20.0, speed=100.0, phi=0.0, name='', command='')
        mock_avoidance.plan_detour.side_effect = [[bypass_wp, target_wp], [bypass_wp2, second_wp]]
        mock_playback.start_streaming.return_value = True

        self.handler.on_start_stream()

        self.assertEqual(mock_avoidance.crosses_dead_zone.call_count, 2)
        self.assertEqual(mock_avoidance.plan_detour.call_count, 2)
        mock_playback.start_streaming.assert_called_once_with(
            [bypass_wp, target_wp, bypass_wp2, second_wp]
        )

    def test_on_pause_resume_stream(self) -> None:
        '''
            Tests toggling pause and catching exception to resume.

            :exceptions: None.
        '''
        mock_playback = self.mocks.playback
        self.handler.on_pause_resume_stream()
        mock_playback.pause_streaming.assert_called_once()

        mock_playback.pause_streaming.side_effect = RuntimeError('Cannot pause')
        self.handler.on_pause_resume_stream()
        mock_playback.resume_streaming.assert_called_once()

    def test_on_stop_stream(self) -> None:
        '''
            Tests aborting and stopping active stream transmission.

            :exceptions: None.
        '''
        mock_playback = self.mocks.playback
        self.handler.on_stop_stream()
        mock_playback.stop_streaming.assert_called_once()


if __name__ == '__main__':
    main()
