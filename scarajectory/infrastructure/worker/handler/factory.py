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
    Factory for creating StreamFrameHandler instances.
'''

from __future__ import annotations

from scarajectory.infrastructure.worker.handler.dependencies import FrameHandlerDependencies
from scarajectory.infrastructure.worker.handler.handler import StreamFrameHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamFrameHandlerFactory:
    '''
        Factory for creating StreamFrameHandler instances.

        It defines:

            :methods:
                | create - Constructs StreamFrameHandler instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        dependencies: FrameHandlerDependencies,
    ) -> StreamFrameHandler:
        '''
            Constructs StreamFrameHandler instance with dependencies.

            :param dependencies: Injected FrameHandlerDependencies parameter bundle.
            :return: Fresh StreamFrameHandler instance.
            :exceptions: None.
        '''
        return StreamFrameHandler(
            flow_pacing=dependencies.flow_pacing,
            state_controller=dependencies.state_controller,
            observer_dispatcher=dependencies.observer_dispatcher,
            response_unpacker=dependencies.response_unpacker,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
