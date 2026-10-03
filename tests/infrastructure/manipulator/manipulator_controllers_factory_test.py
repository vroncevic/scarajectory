# -*- coding: UTF-8 -*-

'''
Module
    manipulator_controllers_factory_test.py
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
    Unit tests for ManipulatorControllersFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.service.connection.iraw_channel import IRawChannel
from scarajectory.infrastructure.gui.controls.\
    manipulator_controllers_bundle import (
        ManipulatorControllersBundle,
    )
from scarajectory.infrastructure.gui.controls.\
    manipulator_controllers_factory import (
        ManipulatorControllersFactory,
    )
from scarajectory.infrastructure.manipulator.jog_controller import JogController
from scarajectory.infrastructure.manipulator.motion_controller import MotionController
from scarajectory.infrastructure.manipulator.query_controller import QueryController
from scarajectory.infrastructure.tool.tool_controller import ToolController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ManipulatorControllersFactoryTestCase(TestCase):
    '''
        Test cases verifying ManipulatorControllersFactory behavior.
    '''

    def setUp(self) -> None:
        self.mock_channel = MagicMock(spec=IRawChannel)

    def test_factory_version(self) -> None:
        '''
            Tests factory version string.
        '''
        self.assertEqual(
            ManipulatorControllersFactory.get_version(), '1.0.4'
        )

    def test_create_bundle_controllers(self) -> None:
        '''
            Tests creation and assembly of 4 manipulator sub-controllers.
        '''
        bundle: ManipulatorControllersBundle = (
            ManipulatorControllersFactory.create(
                raw_channel=self.mock_channel,
                protocol_mode=ProtocolMode.BINARY,
            )
        )
        self.assertIsInstance(bundle, ManipulatorControllersBundle)
        self.assertIsInstance(bundle.motion_ctrl, MotionController)
        self.assertIsInstance(bundle.jog_ctrl, JogController)
        self.assertIsInstance(bundle.tool_ctrl, ToolController)
        self.assertIsInstance(bundle.query_ctrl, QueryController)

    def test_create_bundle_ascii_mode(self) -> None:
        '''
            Tests bundle creation under ASCII protocol mode.
        '''
        bundle: ManipulatorControllersBundle = (
            ManipulatorControllersFactory.create(
                raw_channel=self.mock_channel,
                protocol_mode=ProtocolMode.ASCII,
            )
        )
        self.assertIsInstance(bundle, ManipulatorControllersBundle)
        self.assertIsInstance(bundle.motion_ctrl, MotionController)
        self.assertIsInstance(bundle.jog_ctrl, JogController)


if __name__ == '__main__':
    main()
