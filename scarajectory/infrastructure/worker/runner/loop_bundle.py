# -*- coding: UTF-8 -*-

'''
Module
    loop_bundle.py
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
    Parameter bundle holding collaborators for stream loop execution.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.protocol.iparser import IBinaryFrameParser

from scarajectory.core.model.streaming.pacing_config import StreamPacingConfig
from scarajectory.infrastructure.worker.dispatcher.idispatcher import IStepDispatcher
from scarajectory.infrastructure.worker.drainer.idrainer import IQueueDrainer
from scarajectory.infrastructure.worker.handler.ihandler import IStreamFrameHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class LoopRunnerBundle:
    '''
        Immutable parameter bundle holding collaborators for stream loop execution.

        It defines:

            :attributes:
                | step_dispatcher - IStepDispatcher dispatching waypoints and steps.
                | queue_drainer - IQueueDrainer draining post-loop queue.
                | frame_parser - IBinaryFrameParser decoding inbound frames.
                | frame_handler - IStreamFrameHandler handling responses.
                | pacing_config - StreamPacingConfig with loop pacing delays.
    '''

    step_dispatcher: IStepDispatcher
    queue_drainer: IQueueDrainer
    frame_parser: IBinaryFrameParser
    frame_handler: IStreamFrameHandler
    pacing_config: StreamPacingConfig
