# -*- coding: UTF-8 -*-

'''
Module
    stream_tool_action_handler_test.py
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
    Unit tests for StreamToolActionHandler component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.streaming.handler.stream_tool_action_handler import (
    StreamToolActionHandler,
)
from scarajectory.infrastructure.gui.streaming.streamer_controllers_bundle import (
    StreamerControllersBundle,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStreamToolActionHandler(TestCase):
    '''
        Test cases verifying StreamToolActionHandler commands.

        It defines:

            :methods:
                | setUp - Initializes mock collaborators and handler instance.
                | test_on_home_robot - Tests homing command when connected and disconnected.
                | test_on_toggle_pump - Tests vacuum pump toggle connected and disconnected.
                | test_on_purge_valve - Tests valve pulse connected and disconnected.
                | test_on_override_change - Tests speed override connected and disconnected.
    '''

    def setUp(self) -> None:
        '''Initializes mock collaborators and action handler under test.'''
        self.mock_streamer = MagicMock()
        self.mock_motion = MagicMock()
        self.mock_jog = MagicMock()
        self.mock_tool = MagicMock()
        self.mock_override_panel = MagicMock()

        ctrls = StreamerControllersBundle(
            motion_controller=self.mock_motion,
            jog_controller=self.mock_jog,
            tool_controller=self.mock_tool,
        )
        self.handler = StreamToolActionHandler(
            connection=self.mock_streamer,
            controllers=ctrls,
            override_panel=self.mock_override_panel,
        )

    @patch(
        'scarajectory.infrastructure.gui.streaming.handler.'
        'stream_tool_action_handler.showinfo'
    )
    def test_on_home_robot(self, mock_showinfo: MagicMock) -> None:
        '''Tests homing execution when connected and ignored when disconnected.'''
        self.mock_streamer.is_connected.return_value = True
        self.handler.on_home_robot()
        self.mock_motion.home.assert_called_once()
        mock_showinfo.assert_called_once()

        self.mock_streamer.is_connected.return_value = False
        self.handler.on_home_robot()
        self.assertEqual(self.mock_motion.home.call_count, 1)

    def test_on_toggle_pump(self) -> None:
        '''Tests vacuum pump toggle when connected and ignored when disconnected.'''
        self.mock_streamer.is_connected.return_value = True
        self.handler.on_toggle_pump()
        self.mock_override_panel.set_pump_active.assert_called_once_with(True)
        self.mock_tool.set_pump.assert_called_once_with(True)

        self.mock_streamer.is_connected.return_value = False
        self.handler.on_toggle_pump()
        self.assertEqual(self.mock_tool.set_pump.call_count, 1)

    def test_on_purge_valve(self) -> None:
        '''Tests purge valve pulse when connected and ignored when disconnected.'''
        self.mock_streamer.is_connected.return_value = True
        self.handler.on_purge_valve()
        self.mock_tool.pulse_valve.assert_called_once_with(150)

        self.mock_streamer.is_connected.return_value = False
        self.handler.on_purge_valve()
        self.assertEqual(self.mock_tool.pulse_valve.call_count, 1)

    def test_on_override_change(self) -> None:
        '''Tests feedrate override change when connected and ignored when disconnected.'''
        self.mock_streamer.is_connected.return_value = True
        self.handler.on_override_change('120')
        self.mock_override_panel.set_override_label.assert_called_once_with(120)
        self.mock_jog.set_speed_override.assert_called_once_with(120)

        self.mock_streamer.is_connected.return_value = False
        self.handler.on_override_change('120')
        self.assertEqual(self.mock_jog.set_speed_override.call_count, 1)


if __name__ == '__main__':
    main()
