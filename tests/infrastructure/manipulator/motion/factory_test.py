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
    Unit tests for MotionControllerFactory instantiation service.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scaracom.bridge.transceiver.ichannel import IRawChannel

from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.isystem_builder import IBinarySystemFrameBuilder

from scarajectory.core.service.manipulator.imotion import IMotionController
from scarajectory.infrastructure.connection.dispatcher.idispatcher import IChannelDispatcher
from scarajectory.infrastructure.connection.dispatcher.provides import DispatcherProvides
from scarajectory.infrastructure.manipulator.motion.dependencies import MotionDependencies
from scarajectory.infrastructure.manipulator.motion.factory import MotionControllerFactory
from scarajectory.infrastructure.manipulator.motion.provides import MotionProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionControllerFactoryTestCase(TestCase):
    '''
        Tests verifying MotionControllerFactory creation and version.
    '''

    def test_factory_version(self) -> None:
        '''Verifies factory version string.'''
        self.assertEqual(MotionControllerFactory.get_version(), '1.0.3')

    def test_factory_create(self) -> None:
        '''Verifies constructing MotionProvides via DispatcherFactory.'''
        target_pkg = 'scarajectory.infrastructure.manipulator.motion.factory.'
        with patch(f'{target_pkg}DispatcherFactory.create') as mock_disp_fac:
            mock_disp = MagicMock(spec=IChannelDispatcher)
            mock_disp_fac.return_value = DispatcherProvides(
                channel_dispatcher=mock_disp
            )

            raw_channel = MagicMock(spec=IRawChannel)
            system_builder = MagicMock(spec=IBinarySystemFrameBuilder)
            frame_packer = MagicMock(spec=IBinaryFramePacker)
            deps = MotionDependencies(
                raw_channel=raw_channel,
                system_builder=system_builder,
                frame_packer=frame_packer,
            )

            provides: MotionProvides = MotionControllerFactory.create(deps)

            self.assertIsInstance(provides, MotionProvides)
            self.assertIsInstance(provides.motion_controller, IMotionController)
            mock_disp_fac.assert_called_once()


if __name__ == '__main__':
    main()
