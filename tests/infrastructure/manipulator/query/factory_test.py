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
    Unit tests for QueryControllerFactory instantiation service.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scaracom.bridge.transceiver.ichannel import IRawChannel

from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.isystem_builder import IBinarySystemFrameBuilder

from scarajectory.core.service.manipulator.iquery import IQueryController
from scarajectory.infrastructure.connection.dispatcher.idispatcher import IChannelDispatcher
from scarajectory.infrastructure.connection.dispatcher.provides import DispatcherProvides
from scarajectory.infrastructure.manipulator.query.dependencies import QueryDependencies
from scarajectory.infrastructure.manipulator.query.factory import QueryControllerFactory
from scarajectory.infrastructure.manipulator.query.provides import QueryProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class QueryControllerFactoryTestCase(TestCase):
    '''
        Tests verifying QueryControllerFactory creation and version.
    '''

    def test_factory_version(self) -> None:
        '''Verifies factory version string.'''
        self.assertEqual(QueryControllerFactory.get_version(), '1.0.3')

    def test_factory_create(self) -> None:
        '''Verifies constructing QueryProvides via DispatcherFactory.'''
        target_pkg = 'scarajectory.infrastructure.manipulator.query.factory.'
        with patch(f'{target_pkg}DispatcherFactory.create') as mock_disp_fac:
            mock_disp = MagicMock(spec=IChannelDispatcher)
            mock_disp_fac.return_value = DispatcherProvides(
                channel_dispatcher=mock_disp
            )

            raw_channel = MagicMock(spec=IRawChannel)
            system_builder = MagicMock(spec=IBinarySystemFrameBuilder)
            frame_packer = MagicMock(spec=IBinaryFramePacker)
            deps = QueryDependencies(
                raw_channel=raw_channel,
                system_builder=system_builder,
                frame_packer=frame_packer,
            )

            provides: QueryProvides = QueryControllerFactory.create(deps)

            self.assertIsInstance(provides, QueryProvides)
            self.assertIsInstance(provides.query_controller, IQueryController)
            mock_disp_fac.assert_called_once()


if __name__ == '__main__':
    main()
