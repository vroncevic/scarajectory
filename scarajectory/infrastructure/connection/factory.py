# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Canonical factory service constructing ConnectionProvides subsystem components.
'''

from __future__ import annotations

from scaracom.bridge.dependencies import BridgeDependencies
from scaracom.bridge.factory import BridgeFactory
from scaracom.bridge.provides import BridgeProvides

from scarajectory.infrastructure.connection.dependencies import ConnectionDependencies
from scarajectory.infrastructure.connection.dispatcher.dependencies import DispatcherDependencies
from scarajectory.infrastructure.connection.dispatcher.factory import DispatcherFactory
from scarajectory.infrastructure.connection.dispatcher.provides import DispatcherProvides
from scarajectory.infrastructure.connection.manager.dependencies import ManagerDependencies
from scarajectory.infrastructure.connection.manager.factory import ManagerFactory
from scarajectory.infrastructure.connection.manager.provides import ManagerProvides
from scarajectory.infrastructure.connection.provides import ConnectionProvides
from scarajectory.infrastructure.connection.router.factory import RouterFactory
from scarajectory.infrastructure.connection.router.provides import RouterProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionFactory:
    '''
        Factory providing creation of ConnectionProvides subsystem components.

        It defines:

            :methods:
                | create - Constructs and returns a ConnectionProvides instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: ConnectionDependencies) -> ConnectionProvides:
        '''
            Constructs and returns a ConnectionProvides instance with wired sub-factories.

            :param dependencies: Injected ConnectionDependencies bundle.
            :return: ConnectionProvides instance.
            :exceptions: None.
        '''
        bridge_provides: BridgeProvides = BridgeFactory.create(
            BridgeDependencies(
                transport=dependencies.transport,
                listener=dependencies.listener,
            )
        )
        manager_provides: ManagerProvides = ManagerFactory.create(
            ManagerDependencies(
                connection_coordinator=bridge_provides.coordinator,
            )
        )
        dispatcher_provides: DispatcherProvides = DispatcherFactory.create(
            DispatcherDependencies(
                raw_channel=bridge_provides.transceiver,
                frame_packer=dependencies.frame_packer,
            )
        )
        router_provides: RouterProvides = RouterFactory.create()

        return ConnectionProvides(
            connection_manager=manager_provides.connection_manager,
            raw_channel=bridge_provides.transceiver,
            channel_dispatcher=dispatcher_provides.channel_dispatcher,
            frame_router=router_provides.frame_router,
            connection_coordinator=bridge_provides.coordinator,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
