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
    Unit tests for MotionController adapter.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.service.protocol.isystem_builder import IBinarySystemFrameBuilder

from scarajectory.core.service.manipulator.imotion import IMotionController
from scarajectory.infrastructure.connection.dispatcher.idispatcher import IChannelDispatcher
from scarajectory.infrastructure.manipulator.motion.controller import MotionController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionControllerTestCase(TestCase):
    '''
        Tests verifying MotionController operations in binary mode.
    '''

    def setUp(self) -> None:
        self.mock_dispatcher = MagicMock(spec=IChannelDispatcher)
        self.mock_system_builder = MagicMock(spec=IBinarySystemFrameBuilder)
        self.mock_dispatcher.is_connected.return_value = True
        self.mock_dispatcher.send_frame.return_value = True
        self.mock_dispatcher.next_seq.return_value = 1
        self.mock_frame = MagicMock(spec=BinaryFrame)
        self.mock_system_builder.build_system_cmd.return_value = self.mock_frame

        self.controller = MotionController(
            dispatcher=self.mock_dispatcher,
            system_builder=self.mock_system_builder,
        )

    def test_protocol_satisfaction(self) -> None:
        '''Verifies MotionController satisfies IMotionController protocol.'''
        self.assertIsInstance(self.controller, IMotionController)

    def test_is_connected(self) -> None:
        '''Verifies connectivity delegation.'''
        self.assertTrue(self.controller.is_connected())

    def test_home(self) -> None:
        '''Verifies home routine in binary mode.'''
        result = self.controller.home()
        self.assertTrue(result)
        self.mock_dispatcher.send_frame.assert_called_once_with(self.mock_frame)

    def test_enable(self) -> None:
        '''Verifies enable routine in binary mode.'''
        result = self.controller.enable()
        self.assertTrue(result)
        self.mock_dispatcher.send_frame.assert_called_once_with(self.mock_frame)

    def test_disable(self) -> None:
        '''Verifies disable routine in binary mode.'''
        result = self.controller.disable()
        self.assertTrue(result)
        self.mock_dispatcher.send_frame.assert_called_once_with(self.mock_frame)

    def test_clear_fault(self) -> None:
        '''Verifies clear fault routine in binary mode.'''
        result = self.controller.clear_fault()
        self.assertTrue(result)
        self.mock_dispatcher.send_frame.assert_called_once_with(self.mock_frame)


if __name__ == '__main__':
    main()
