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
    Unit tests for ManipulatorFactory subsystem instantiation service.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scaracom.bridge.transceiver.ichannel import IRawChannel

from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.isystem_builder import IBinarySystemFrameBuilder

from scarajectory.core.service.manipulator.ijog import IJogController
from scarajectory.core.service.manipulator.imotion import IMotionController
from scarajectory.core.service.manipulator.iquery import IQueryController
from scarajectory.infrastructure.manipulator.dependencies import ManipulatorDependencies
from scarajectory.infrastructure.manipulator.factory import ManipulatorFactory
from scarajectory.infrastructure.manipulator.jog.provides import JogProvides
from scarajectory.infrastructure.manipulator.motion.provides import MotionProvides
from scarajectory.infrastructure.manipulator.provides import ManipulatorProvides
from scarajectory.infrastructure.manipulator.query.provides import QueryProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ManipulatorFactoryTestCase(TestCase):
    '''
        Tests verifying ManipulatorFactory component creation and version.
    '''

    def test_factory_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        self.assertEqual(ManipulatorFactory.get_version(), '1.0.3')

    def test_factory_create(self) -> None:
        '''
            Verifies assembling sub-controllers into ManipulatorProvides.

            :exceptions: None.
        '''
        target_pkg = 'scarajectory.infrastructure.manipulator.factory.'
        with (
            patch(f'{target_pkg}JogControllerFactory.create') as mock_jog_fac,
            patch(f'{target_pkg}MotionControllerFactory.create') as mock_mot_fac,
            patch(f'{target_pkg}QueryControllerFactory.create') as mock_qry_fac,
        ):
            mock_jog = MagicMock(spec=IJogController)
            mock_motion = MagicMock(spec=IMotionController)
            mock_query = MagicMock(spec=IQueryController)

            mock_jog_fac.return_value = JogProvides(jog_controller=mock_jog)
            mock_mot_fac.return_value = MotionProvides(motion_controller=mock_motion)
            mock_qry_fac.return_value = QueryProvides(query_controller=mock_query)

            raw_channel = MagicMock(spec=IRawChannel)
            system_builder = MagicMock(spec=IBinarySystemFrameBuilder)
            frame_packer = MagicMock(spec=IBinaryFramePacker)
            deps = ManipulatorDependencies(
                raw_channel=raw_channel,
                system_builder=system_builder,
                frame_packer=frame_packer,
            )

            provides: ManipulatorProvides = ManipulatorFactory.create(deps)

            self.assertIsInstance(provides, ManipulatorProvides)
            self.assertIs(provides.jog_controller, mock_jog)
            self.assertIs(provides.motion_controller, mock_motion)
            self.assertIs(provides.query_controller, mock_query)
            mock_jog_fac.assert_called_once()
            mock_mot_fac.assert_called_once()
            mock_qry_fac.assert_called_once()


if __name__ == '__main__':
    main()
