# -*- coding: UTF-8 -*-

'''
Module
    istream_line_receiver.py
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
    Defines structural protocol IStreamLineReceiver for incoming text response line reception.
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
class IStreamLineReceiver(Protocol):
    '''
    Structural protocol defining consumption of incoming ASCII response lines.

    It defines:

        :methods:
            | handle_incoming_line - Ingests and processes incoming text response line.
            | is_running - Checks whether the receiver is active.
    '''

    def handle_incoming_line(self, line: str) -> None:
        '''
        Ingests and processes incoming text response line.

        :param line: Raw response line string received from microcontroller.
        '''

    def is_running(self) -> bool:
        '''
        Checks whether the receiver is active.

        :return: True if active, False otherwise.
        '''
