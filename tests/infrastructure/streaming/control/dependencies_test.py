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
    Unit testing for ControlDependencies dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaracom.bridge.transceiver.ichannel import IRawChannel

from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.isystem_builder import IBinarySystemFrameBuilder

from scarajectory.infrastructure.streaming.control.dependencies import ControlDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestControlDependencies(TestCase):
    '''
    Test cases verifying ControlDependencies dataclass.

    It defines:

        :methods:
            | test_initialization - Tests attributes and immutability.
    '''

    def test_initialization(self) -> None:
        '''Tests dataclass property storage and immutability.'''
        raw_xceiver = MagicMock(spec=IRawChannel)
        mock_builder = MagicMock(spec=IBinarySystemFrameBuilder)
        mock_packer = MagicMock(spec=IBinaryFramePacker)
        deps = ControlDependencies(
            raw_transceiver=raw_xceiver,
            system_builder=mock_builder,
            frame_packer=mock_packer,
        )
        self.assertIs(deps.raw_transceiver, raw_xceiver)
        self.assertIs(deps.system_builder, mock_builder)
        self.assertIs(deps.frame_packer, mock_packer)


if __name__ == '__main__':
    main()
