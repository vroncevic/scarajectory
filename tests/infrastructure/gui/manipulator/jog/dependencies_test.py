# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for JogDependencies.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.manipulator.jog.dependencies import JogDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJogDependencies(TestCase):
    '''
        Test cases verifying JogDependencies instantiation and property access.
    '''

    def test_dependencies_properties(self) -> None:
        '''
            Tests dependencies attributes assignment.

            :exceptions: None.
        '''
        mock_channel = MagicMock()
        mock_motion = MagicMock()
        mock_jog = MagicMock()
        mock_tool = MagicMock()
        mock_query = MagicMock()

        deps = JogDependencies(
            raw_channel=mock_channel,
            motion_controller=mock_motion,
            jog_controller=mock_jog,
            tool_controller=mock_tool,
            query_controller=mock_query,
        )

        self.assertIs(deps.raw_channel, mock_channel)
        self.assertIs(deps.motion_controller, mock_motion)
        self.assertIs(deps.jog_controller, mock_jog)
        self.assertIs(deps.tool_controller, mock_tool)
        self.assertIs(deps.query_controller, mock_query)


if __name__ == '__main__':
    main()
