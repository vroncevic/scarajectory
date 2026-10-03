# -*- coding: UTF-8 -*-

'''
Module
    iflow_barrier_coordinator.py
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
    Defines structural protocol IFlowBarrierCoordinator for flow barrier coordination.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IFlowBarrierCoordinator(Protocol):
    '''
        Structural protocol defining flow barrier coordination operations.

        It defines:

            :methods:
                | set_barrier - Locks synchronization barrier for command gating.
                | clear_barrier - Unlocks synchronization barrier.
                | is_barrier_clear - Checks whether synchronization barrier is unlocked.
                | reset - Resets barrier to initial cleared state.
    '''

    def set_barrier(self) -> None:
        '''
            Locks synchronization barrier for command gating.
        '''

    def clear_barrier(self) -> None:
        '''
            Unlocks synchronization barrier.
        '''

    def is_barrier_clear(self) -> bool:
        '''
            Checks whether synchronization barrier is unlocked.

            :return: True if barrier is clear, False otherwise.
        '''

    def reset(self) -> None:
        '''
            Resets barrier to initial cleared state.
        '''
