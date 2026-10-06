# -*- coding: UTF-8 -*-

'''
Module
    manipulator_controllers_bundle_test.py
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
    Unit tests for ManipulatorControllersBundle data container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.controls.manipulator_controllers_bundle import ManipulatorControllersBundle
from scarajectory.infrastructure.manipulator.jog_controller import JogController
from scarajectory.infrastructure.manipulator.motion_controller import MotionController
from scarajectory.infrastructure.manipulator.query_controller import QueryController
from scarajectory.infrastructure.tool.tool_controller import ToolController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ManipulatorControllersBundleTestCase(TestCase):
    '''
        Tests ManipulatorControllersBundle creation and immutability.

        It defines:

            :methods:
                | test_bundle_creation_and_attributes - Verifies attribute assignments.
                | test_bundle_immutability - Verifies frozen dataclass behavior.
    '''

    def test_bundle_creation_and_attributes(self) -> None:
        '''Verifies all controller attributes are properly preserved.'''
        mock_motion = MagicMock(spec=MotionController)
        mock_jog = MagicMock(spec=JogController)
        mock_tool = MagicMock(spec=ToolController)
        mock_query = MagicMock(spec=QueryController)

        bundle = ManipulatorControllersBundle(
            motion_ctrl=mock_motion,
            jog_ctrl=mock_jog,
            tool_ctrl=mock_tool,
            query_ctrl=mock_query,
        )

        self.assertIs(bundle.motion_ctrl, mock_motion)
        self.assertIs(bundle.jog_ctrl, mock_jog)
        self.assertIs(bundle.tool_ctrl, mock_tool)
        self.assertIs(bundle.query_ctrl, mock_query)

    def test_bundle_immutability(self) -> None:
        '''Verifies modifying attributes raises FrozenInstanceError.'''
        bundle = ManipulatorControllersBundle(
            motion_ctrl=MagicMock(spec=MotionController),
            jog_ctrl=MagicMock(spec=JogController),
            tool_ctrl=MagicMock(spec=ToolController),
            query_ctrl=MagicMock(spec=QueryController),
        )

        with self.assertRaises(FrozenInstanceError):
            bundle.motion_ctrl = MagicMock(spec=MotionController)  # type: ignore[misc]


if __name__ == '__main__':
    main()
