# -*- coding: UTF-8 -*-

'''
Module
    flow_barrier_coordinator.py
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
    Coordinates thread synchronization barrier operations for command execution gating.
'''

from __future__ import annotations

from typing import Final

from scarajectory.infrastructure.barrier.iflow_barrier import IFlowBarrier

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FlowBarrierCoordinator:
    '''
        Coordinates thread synchronization barrier operations for command execution gating.

        It defines:

            :attributes:
                | _barrier - Injected IFlowBarrier managing synchronization events.
            :methods:
                | __init__ - Initializes barrier coordinator with injected IFlowBarrier.
                | set_barrier - Locks synchronization barrier for command gating.
                | clear_barrier - Unlocks synchronization barrier.
                | is_barrier_clear - Checks whether synchronization barrier is unlocked.
                | reset - Resets barrier to initial cleared state.
    '''

    _barrier: IFlowBarrier

    def __init__(self, barrier: IFlowBarrier) -> None:
        '''
            Initializes barrier coordinator with injected IFlowBarrier.

            :param barrier: Injected IFlowBarrier instance.
            :exceptions: None.
        '''
        self._barrier: Final[IFlowBarrier] = barrier

    def set_barrier(self) -> None:
        '''
            Locks synchronization barrier for command gating.

            :exceptions: None.
        '''
        self._barrier.set_barrier()

    def clear_barrier(self) -> None:
        '''
            Unlocks synchronization barrier.

            :exceptions: None.
        '''
        self._barrier.clear_barrier()

    def is_barrier_clear(self) -> bool:
        '''
            Checks whether synchronization barrier is unlocked.

            :return: True if barrier is clear, False otherwise.
            :exceptions: None.
        '''
        return self._barrier.is_barrier_clear()

    def reset(self) -> None:
        '''
            Resets barrier to initial cleared state.

            :exceptions: None.
        '''
        self._barrier.reset()
