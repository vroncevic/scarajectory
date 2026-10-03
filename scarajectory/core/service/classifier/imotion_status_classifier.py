# -*- coding: UTF-8 -*-

'''
Module
    imotion_status_classifier.py
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
    Defines IMotionStatusClassifier protocol interface for waypoint moves and auxiliary actions.
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
class IMotionStatusClassifier(Protocol):
    '''
        Protocol contract for evaluating waypoint motion and auxiliary action completion.

        It defines:

            :methods:
                | is_move_done - Checks if packet confirms completion of a waypoint move.
                | is_move_failed - Checks if packet confirms failure of a waypoint move.
                | is_action_done - Checks if packet confirms completion of a tool or wait action.
                | is_complete - Checks if packet confirms completion of either a move or action.
    '''

    def is_move_done(self, line: str) -> bool:
        '''
            Checks if packet confirms completion of a waypoint move.

            :param line: Received line string.
            :return: True if move completed confirmation, False otherwise.
        '''

    def is_move_failed(self, line: str) -> bool:
        '''
            Checks if packet confirms failure of a waypoint move.

            :param line: Received line string.
            :return: True if move failed confirmation, False otherwise.
        '''

    def is_action_done(self, line: str) -> bool:
        '''
            Checks if packet confirms completion of a tool, wait, or auxiliary action.

            :param line: Received line string.
            :return: True if action completion confirmation, False otherwise.
        '''

    def is_complete(self, line: str) -> bool:
        '''
            Checks if packet confirms completion of either a waypoint move or action.

            :param line: Received line string.
            :return: True if move or action completed, False otherwise.
        '''
