# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit testing for ControlFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaracom.bridge.transceiver.ichannel import IRawChannel

from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.isystem_builder import IBinarySystemFrameBuilder

from scarajectory.core.service.streaming.control.itransmitter import IControlTransmitter
from scarajectory.infrastructure.streaming.control.dependencies import ControlDependencies
from scarajectory.infrastructure.streaming.control.factory import ControlFactory
from scarajectory.infrastructure.streaming.control.provides import ControlProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestControlFactory(TestCase):
    '''
    Test cases verifying ControlFactory.

    It defines:

        :methods:
            | test_create - Tests factory creates ControlProvides with valid transmitter.
            | test_get_version - Tests factory version string.
    '''

    def test_create(self) -> None:
        '''
            Tests factory creation of ControlProvides.

            :exceptions: None.
        '''
        raw_xceiver = MagicMock(spec=IRawChannel)
        mock_builder = MagicMock(spec=IBinarySystemFrameBuilder)
        mock_packer = MagicMock(spec=IBinaryFramePacker)
        deps = ControlDependencies(
            raw_transceiver=raw_xceiver,
            system_builder=mock_builder,
            frame_packer=mock_packer,
        )
        provides: ControlProvides = ControlFactory.create(deps)
        self.assertIsInstance(provides, ControlProvides)
        self.assertIsInstance(provides.control_transmitter, IControlTransmitter)

    def test_get_version(self) -> None:
        '''
            Tests version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(ControlFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
