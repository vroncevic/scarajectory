# -*- coding: UTF-8 -*-

'''
Module
    controller_test.py
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
    Unit testing for ToolController component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.service.protocol.iactuator_builder import IBinaryActuatorFrameBuilder

from scarajectory.core.service.tool.iactuator import IPurgeValveActuator
from scarajectory.core.service.tool.icontroller import IToolController
from scarajectory.infrastructure.connection.dispatcher.idispatcher import IChannelDispatcher
from scarajectory.infrastructure.tool.controller.controller import ToolController
from scarajectory.infrastructure.tool.worker.irunner import IValvePulseRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolController(TestCase):
    '''
        Unit tests validating ToolController actuation methods and protocol compliance.

        It defines:

            :methods:
                | test_protocols_conformance - Verifies structural protocols.
                | test_is_connected - Verifies connectivity delegation.
                | test_set_vacuum_pump - Verifies vacuum pump in BINARY mode.
                | test_set_valve - Verifies valve in BINARY mode.
                | test_pulse_and_deactivate_purge_valve - Verifies pulse and deactivation.
    '''

    def test_protocols_conformance(self) -> None:
        '''
            Verifies ToolController satisfies IToolController and IPurgeValveActuator.

            :exceptions: None.
        '''
        dispatcher = MagicMock(spec=IChannelDispatcher)
        builder = MagicMock(spec=IBinaryActuatorFrameBuilder)
        runner = MagicMock(spec=IValvePulseRunner)

        ctrl = ToolController(
            dispatcher=dispatcher,
            actuator_builder=builder,
            pulse_runner=runner,
        )
        self.assertIsInstance(ctrl, IToolController)
        self.assertIsInstance(ctrl, IPurgeValveActuator)

    def test_is_connected(self) -> None:
        '''
            Verifies is_connected delegation.

            :exceptions: None.
        '''
        dispatcher = MagicMock(spec=IChannelDispatcher)
        dispatcher.is_connected.return_value = True
        builder = MagicMock(spec=IBinaryActuatorFrameBuilder)
        runner = MagicMock(spec=IValvePulseRunner)

        ctrl = ToolController(
            dispatcher=dispatcher,
            actuator_builder=builder,
            pulse_runner=runner,
        )
        self.assertTrue(ctrl.is_connected())

    def test_set_vacuum_pump(self) -> None:
        '''
            Verifies vacuum pump actuation in BINARY mode.

            :exceptions: None.
        '''
        dispatcher = MagicMock(spec=IChannelDispatcher)
        dispatcher.send_frame.return_value = True
        builder = MagicMock(spec=IBinaryActuatorFrameBuilder)
        runner = MagicMock(spec=IValvePulseRunner)
        mock_frame = MagicMock(spec=BinaryFrame)
        builder.build_tool_cmd.return_value = mock_frame

        ctrl = ToolController(
            dispatcher=dispatcher,
            actuator_builder=builder,
            pulse_runner=runner,
        )

        success = ctrl.set_vacuum_pump(True)
        self.assertTrue(success)
        builder.build_tool_cmd.assert_called_once()
        dispatcher.send_frame.assert_called_once_with(mock_frame)

    def test_set_valve(self) -> None:
        '''
            Verifies purge valve actuation in BINARY mode.

            :exceptions: None.
        '''
        dispatcher = MagicMock(spec=IChannelDispatcher)
        dispatcher.send_frame.return_value = True
        builder = MagicMock(spec=IBinaryActuatorFrameBuilder)
        runner = MagicMock(spec=IValvePulseRunner)
        mock_frame = MagicMock(spec=BinaryFrame)
        builder.build_tool_cmd.return_value = mock_frame

        ctrl = ToolController(
            dispatcher=dispatcher,
            actuator_builder=builder,
            pulse_runner=runner,
        )

        success = ctrl.set_valve(True)
        self.assertTrue(success)
        builder.build_tool_cmd.assert_called_once()
        dispatcher.send_frame.assert_called_once_with(mock_frame)

    def test_pulse_and_deactivate_purge_valve(self) -> None:
        '''
            Verifies pulse_purge_valve initiates runner and deactivate resets valve.

            :exceptions: None.
        '''
        dispatcher = MagicMock(spec=IChannelDispatcher)
        dispatcher.is_connected.return_value = False
        dispatcher.send_frame.return_value = True
        builder = MagicMock(spec=IBinaryActuatorFrameBuilder)
        runner = MagicMock(spec=IValvePulseRunner)
        mock_frame = MagicMock(spec=BinaryFrame)
        builder.build_tool_cmd.return_value = mock_frame

        ctrl = ToolController(
            dispatcher=dispatcher,
            actuator_builder=builder,
            pulse_runner=runner,
        )

        self.assertFalse(ctrl.pulse_purge_valve())
        runner.schedule_deactivation.assert_not_called()

        dispatcher.is_connected.return_value = True
        self.assertTrue(ctrl.pulse_purge_valve())
        runner.schedule_deactivation.assert_called_once_with(
            actuator=ctrl,
            delay_sec=ToolController.PULSE_DELAY_SEC,
        )

        ctrl.deactivate_purge_valve()
        dispatcher.send_frame.assert_called_with(mock_frame)


if __name__ == '__main__':
    main()
