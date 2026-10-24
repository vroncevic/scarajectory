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
    Unit tests for ToolDependencies dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaracom.bridge.transceiver.ichannel import IRawChannel

from scaralang.core.service.protocol.iactuator_builder import IBinaryActuatorFrameBuilder
from scaralang.core.service.protocol.ipacker import IBinaryFramePacker

from scarajectory.infrastructure.tool.dependencies import ToolDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolDependencies(TestCase):
    '''
    Test cases verifying ToolDependencies immutability and attributes.

    It defines:

        :methods:
            | test_bundle_creation - Verifies valid attribute storage.
            | test_bundle_frozen - Verifies dataclass immutability.
    '''

    def test_bundle_creation(self) -> None:
        '''
        Verifies bundle correctly holds provided dependencies.
        '''
        mock_raw = MagicMock(spec=IRawChannel)
        mock_actuator = MagicMock(spec=IBinaryActuatorFrameBuilder)
        mock_packer = MagicMock(spec=IBinaryFramePacker)

        deps = ToolDependencies(
            raw_channel=mock_raw,
            actuator_builder=mock_actuator,
            frame_packer=mock_packer,
        )
        self.assertIs(deps.raw_channel, mock_raw)
        self.assertIs(deps.actuator_builder, mock_actuator)
        self.assertIs(deps.frame_packer, mock_packer)

    def test_bundle_frozen(self) -> None:
        '''
        Verifies that modifying attributes raises an error due to frozen dataclass.
        '''
        mock_raw = MagicMock(spec=IRawChannel)
        mock_actuator = MagicMock(spec=IBinaryActuatorFrameBuilder)
        mock_packer = MagicMock(spec=IBinaryFramePacker)

        deps = ToolDependencies(
            raw_channel=mock_raw,
            actuator_builder=mock_actuator,
            frame_packer=mock_packer,
        )
        with self.assertRaises(AttributeError):
            deps.raw_channel = mock_raw  # type: ignore[misc]


if __name__ == '__main__':
    main()
