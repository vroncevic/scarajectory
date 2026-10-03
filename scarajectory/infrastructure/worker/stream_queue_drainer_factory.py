# -*- coding: UTF-8 -*-

'''
Module
    stream_queue_drainer_factory.py
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
    Factory constructing StreamQueueDrainer instances.
'''

from __future__ import annotations

from scarajectory.core.model.streaming.stream_pacing_config import StreamPacingConfig
from scarajectory.core.service.state.istream_state_controller import IStreamStateController
from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.worker.stream_queue_drainer import StreamQueueDrainer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamQueueDrainerFactory:
    '''
        Factory constructing StreamQueueDrainer instances.

        It defines:

            :methods:
                | create - Constructs and returns StreamQueueDrainer.
                | get_version - Returns factory module semantic version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        state_controller: IStreamStateController,
        observer_dispatcher: IStreamObserverDispatcher,
        pacing_config: StreamPacingConfig,
    ) -> StreamQueueDrainer:
        '''
            Constructs and returns StreamQueueDrainer.

            :param state_controller: Controller managing streaming state.
            :param observer_dispatcher: Dispatcher publishing telemetry.
            :param pacing_config: Pacing configuration with poll delay.
            :return: Configured StreamQueueDrainer instance.
            :exceptions: None.
        '''
        return StreamQueueDrainer(
            state_controller=state_controller,
            observer_dispatcher=observer_dispatcher,
            pacing_config=pacing_config,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory module semantic version string.

            :return: Semantic version string (__version__).
            :exceptions: None.
        '''
        return __version__
