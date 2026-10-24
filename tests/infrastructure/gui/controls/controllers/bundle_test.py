# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit tests for TabControllersBundle data container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.manipulator.ijog import IJogController
from scarajectory.core.service.manipulator.imotion import IMotionController
from scarajectory.core.service.manipulator.iquery import IQueryController
from scarajectory.core.service.tool.icontroller import IToolController
from scarajectory.infrastructure.gui.controls.controllers.bundle import TabControllersBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TabControllersBundleTestCase(TestCase):
    '''
        Tests TabControllersBundle creation and immutability.

        It defines:

            :methods:
                | test_bundle_creation_and_attributes - Verifies attribute assignments.
                | test_bundle_immutability - Verifies frozen dataclass behavior.
    '''

    def test_bundle_creation_and_attributes(self) -> None:
        '''
            Verifies all controller attributes are properly preserved.

            :exceptions: None.
        '''
        mock_motion = MagicMock(spec=IMotionController)
        mock_jog = MagicMock(spec=IJogController)
        mock_tool = MagicMock(spec=IToolController)
        mock_query = MagicMock(spec=IQueryController)

        bundle = TabControllersBundle(
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
        '''
            Verifies modifying attributes raises FrozenInstanceError.

            :exceptions: None.
        '''
        bundle = TabControllersBundle(
            motion_ctrl=MagicMock(spec=IMotionController),
            jog_ctrl=MagicMock(spec=IJogController),
            tool_ctrl=MagicMock(spec=IToolController),
            query_ctrl=MagicMock(spec=IQueryController),
        )

        with self.assertRaises(FrozenInstanceError):
            bundle.motion_ctrl = MagicMock(spec=IMotionController)  # type: ignore[misc]


if __name__ == '__main__':
    main()
