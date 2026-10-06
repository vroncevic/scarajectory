# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Immutable value bundle holding flow pacing and barrier coordination dependencies.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.infrastructure.pacing.iflow_barrier_coordinator import IFlowBarrierCoordinator
from scarajectory.infrastructure.pacing.iflow_pacing_controller import IFlowPacingController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class FlowPacingBundle:
    '''
        Value object bundling flow pacing controller and barrier coordinator.

        It defines:

            :attributes:
                | pacing_controller - Injected IFlowPacingController managing rate pacing.
                | barrier_coordinator - Injected IFlowBarrierCoordinator managing synchronization.
    '''

    pacing_controller: IFlowPacingController
    barrier_coordinator: IFlowBarrierCoordinator
