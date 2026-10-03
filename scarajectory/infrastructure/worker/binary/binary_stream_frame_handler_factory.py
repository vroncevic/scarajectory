# -*- coding: UTF-8 -*-

'''
Module
    binary_stream_frame_handler_factory.py
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
    Factory for creating BinaryStreamFrameHandler instances.
'''

from __future__ import annotations

from scarajectory.core.service.pacing.iflow_pacing_controller import IFlowPacingController
from scarajectory.core.service.state.istream_state_controller import IStreamStateController
from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.worker.binary.binary_stream_frame_handler import BinaryStreamFrameHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStreamFrameHandlerFactory:
    '''
        Factory for creating BinaryStreamFrameHandler instances.

        It defines:

            :methods:
                | create - Constructs BinaryStreamFrameHandler instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        flow_pacing: IFlowPacingController,
        state_controller: IStreamStateController,
        observer_dispatcher: IStreamObserverDispatcher,
    ) -> BinaryStreamFrameHandler:
        '''
            Constructs BinaryStreamFrameHandler instance with dependencies.

            :param flow_pacing: Injected IFlowPacingController instance.
            :param state_controller: Injected IStreamStateController instance.
            :param observer_dispatcher: Injected IStreamObserverDispatcher instance.
            :return: Fresh BinaryStreamFrameHandler instance.
            :exceptions: None.
        '''
        return BinaryStreamFrameHandler(
            flow_pacing=flow_pacing,
            state_controller=state_controller,
            observer_dispatcher=observer_dispatcher,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
