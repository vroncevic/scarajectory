# -*- coding: UTF-8 -*-

'''
Module
    receiver.py
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
    Ingests and processes raw incoming bytes from stream transport.
'''

from __future__ import annotations

from typing import Final

from scarajectory.infrastructure.worker.holder import StreamSessionHolder
from scarajectory.infrastructure.worker.iexecution_worker import IExecutionWorker
from scarajectory.infrastructure.worker.runner.irunner import IStreamLoopRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamBytesReceiver:
    '''
        Ingests and processes raw incoming bytes from stream transport.

        It defines:

            :attributes:
                | _loop_runner - IStreamLoopRunner managing step execution loops.
                | _worker - IExecutionWorker managing streaming execution lifecycle.
                | _session_holder - StreamSessionHolder tracking active stream session.
            :methods:
                | __init__ - Initializes receiver with injected collaborators.
                | handle_incoming_bytes - Ingests and processes incoming raw byte chunk.
                | is_running - Checks whether the receiver is active.
    '''

    _loop_runner: IStreamLoopRunner
    _worker: IExecutionWorker
    _session_holder: StreamSessionHolder

    def __init__(
        self,
        *,
        loop_runner: IStreamLoopRunner,
        worker: IExecutionWorker,
        session_holder: StreamSessionHolder,
    ) -> None:
        '''
            Initializes receiver with loop runner, execution worker, and session holder.

            :param loop_runner: Injected IStreamLoopRunner instance.
            :param worker: Injected IExecutionWorker instance.
            :param session_holder: Injected StreamSessionHolder instance.
            :exceptions: None.
        '''
        self._loop_runner: Final[IStreamLoopRunner] = loop_runner
        self._worker: Final[IExecutionWorker] = worker
        self._session_holder: Final[StreamSessionHolder] = session_holder

    def handle_incoming_bytes(self, data: bytes) -> None:
        '''
            Ingests and processes incoming raw byte chunk.

            :param data: Byte chunk received from communication transport.
            :exceptions: None.
        '''
        should_stop: bool = self._loop_runner.handle_incoming_bytes(
            data=data, session=self._session_holder.session
        )
        if should_stop:
            self._worker.stop()

    def is_running(self) -> bool:
        '''
            Checks whether the receiver is active.

            :return: True if active, False otherwise.
            :exceptions: None.
        '''
        return self._worker.is_running()
