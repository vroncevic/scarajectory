# -*- coding: UTF-8 -*-

'''
Module
    imotion_controller.py
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
    Defines structural protocol IMotionController for robot power and homing operations.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMotionController(Protocol):
    '''
        Structural protocol defining robot power, homing, and fault recovery operations.

        It defines:

            :methods:
                | home - Executes robot homing sequence.
                | enable - Energizes and enables joint stepper motors.
                | disable - De-energizes joint stepper motors.
                | clear_fault - Clears latched fault state.
    '''

    def home(self) -> bool:
        '''
            Executes robot homing sequence.

            :return: True if command transmitted successfully, False otherwise.
        '''

    def enable(self) -> bool:
        '''
            Energizes and enables joint stepper motors.

            :return: True if command transmitted successfully, False otherwise.
        '''

    def disable(self) -> bool:
        '''
            De-energizes joint stepper motors.

            :return: True if command transmitted successfully, False otherwise.
        '''

    def clear_fault(self) -> bool:
        '''
            Clears latched hardware fault state.

            :return: True if command transmitted successfully, False otherwise.
        '''
