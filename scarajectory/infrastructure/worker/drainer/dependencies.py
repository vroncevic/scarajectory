# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Parameter bundle dependencies for QueueDrainer component.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.model.streaming.pacing_config import StreamPacingConfig
from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.state.imachine import IStreamStateMachine

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class QueueDrainerDependencies:
    '''
        Parameter bundle encapsulating external collaborators for QueueDrainer.

        It defines:

            :attributes:
                | state_controller - Injected IStreamStateMachine managing streaming state.
                | observer_dispatcher - Dispatcher publishing telemetry.
                | pacing_config - Pacing configuration with poll delay.
    '''

    state_controller: IStreamStateMachine
    observer_dispatcher: IStreamObserverDispatcher
    pacing_config: StreamPacingConfig
