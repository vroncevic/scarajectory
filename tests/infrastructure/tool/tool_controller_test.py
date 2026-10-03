# -*- coding: UTF-8 -*-

'''
Module
    tool_controller_test.py
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
    Unit testing for ToolController and ToolControllerFactory components.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.infrastructure.tool.tool_controller import ToolController
from scarajectory.infrastructure.tool.tool_controller_factory import ToolControllerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolControllerTestCase(TestCase):
    '''Unit tests validating ToolController actuation methods and factory creation.'''

    def test_connection_and_protocol_mode(self) -> None:
        '''Verifies is_connected delegation and set_protocol_mode updates.'''
        dispatcher = MagicMock()
        dispatcher.is_connected.return_value = True
        builder = MagicMock()
        worker_factory = MagicMock()

        ctrl = ToolController(
            dispatcher=dispatcher,
            frame_builder=builder,
            worker_factory=worker_factory,
        )
        self.assertTrue(ctrl.is_connected())

        ctrl.set_protocol_mode(ProtocolMode.ASCII)
        self.assertEqual(dispatcher.protocol_mode, ProtocolMode.ASCII)

    def test_set_vacuum_pump_modes(self) -> None:
        '''Verifies vacuum pump actuation in both ASCII and BINARY modes.'''
        dispatcher = MagicMock()
        dispatcher.protocol_mode = ProtocolMode.ASCII
        dispatcher.send_command.return_value = True
        dispatcher.send_frame.return_value = True
        builder = MagicMock()
        builder.build_tool_cmd.return_value = MagicMock()
        worker_factory = MagicMock()

        ctrl = ToolController(
            dispatcher=dispatcher,
            frame_builder=builder,
            worker_factory=worker_factory,
        )

        success_ascii = ctrl.set_vacuum_pump(True)
        self.assertTrue(success_ascii)
        dispatcher.send_command.assert_called_once_with('<CMD:PUMP#1>')

        dispatcher.protocol_mode = ProtocolMode.BINARY
        success_bin = ctrl.set_vacuum_pump(False)
        self.assertTrue(success_bin)
        builder.build_tool_cmd.assert_called_once()
        dispatcher.send_frame.assert_called_once()

    def test_set_valve_modes(self) -> None:
        '''Verifies purge valve actuation in both ASCII and BINARY modes.'''
        dispatcher = MagicMock()
        dispatcher.protocol_mode = ProtocolMode.ASCII
        dispatcher.send_command.return_value = True
        dispatcher.send_frame.return_value = True
        builder = MagicMock()
        builder.build_tool_cmd.return_value = MagicMock()
        worker_factory = MagicMock()

        ctrl = ToolController(
            dispatcher=dispatcher,
            frame_builder=builder,
            worker_factory=worker_factory,
        )

        success_ascii = ctrl.set_valve(True)
        self.assertTrue(success_ascii)
        dispatcher.send_command.assert_called_once_with('<CMD:VALVE#1>')

        dispatcher.protocol_mode = ProtocolMode.BINARY
        success_bin = ctrl.set_valve(False)
        self.assertTrue(success_bin)
        builder.build_tool_cmd.assert_called_once()
        dispatcher.send_frame.assert_called_once()

    def test_pulse_and_deactivate_purge_valve(self) -> None:
        '''Verifies pulse_purge_valve initiates worker and deactivate resets valve.'''
        dispatcher = MagicMock()
        dispatcher.is_connected.return_value = False
        dispatcher.protocol_mode = ProtocolMode.ASCII
        builder = MagicMock()
        mock_worker = MagicMock()
        worker_factory = MagicMock()
        worker_factory.create.return_value = mock_worker

        ctrl = ToolController(
            dispatcher=dispatcher,
            frame_builder=builder,
            worker_factory=worker_factory,
        )

        self.assertFalse(ctrl.pulse_purge_valve())

        dispatcher.is_connected.return_value = True
        self.assertTrue(ctrl.pulse_purge_valve())
        worker_factory.create.assert_called_once()
        mock_worker.start.assert_called_once()

        ctrl.deactivate_purge_valve()
        dispatcher.send_command.assert_called_with('<CMD:VALVE#0>')

    def test_factory_creation_and_version(self) -> None:
        '''Verifies ToolControllerFactory instantiates ToolController and reports version.'''
        raw_channel = MagicMock()
        builder = MagicMock()
        ctrl = ToolControllerFactory.create(
            raw_channel=raw_channel,
            frame_builder=builder,
            protocol_mode=ProtocolMode.ASCII,
        )
        self.assertIsInstance(ctrl, ToolController)
        self.assertEqual(ToolControllerFactory.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
