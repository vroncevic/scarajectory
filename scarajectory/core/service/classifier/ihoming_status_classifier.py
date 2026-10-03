# -*- coding: UTF-8 -*-

'''
Module
    ihoming_status_classifier.py
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
    Defines IHomingStatusClassifier protocol interface for machine homing and calibration verification.
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
class IHomingStatusClassifier(Protocol):
    '''
        Protocol contract for verifying machine homing routine success and failure packets.

        It defines:

            :methods:
                | is_homed_success - Checks if packet confirms successful robot homing.
                | is_homing_failed - Checks if packet confirms homing failure or timeout.
    '''

    def is_homed_success(self, line: str) -> bool:
        '''
            Checks if packet confirms successful robot homing.

            :param line: Received line string.
            :return: True if homing succeeded, False otherwise.
        '''

    def is_homing_failed(self, line: str) -> bool:
        '''
            Checks if packet confirms homing failure or timeout.

            :param line: Received line string.
            :return: True if homing failed, False otherwise.
        '''
