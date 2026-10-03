# -*- coding: UTF-8 -*-

'''
Module
    ijog_controller.py
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
    Defines structural protocol IJogController for manual jogging and feedrate override.
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
class IJogController(Protocol):
    '''
        Structural protocol defining manual jogging and feedrate override operations.

        It defines:

            :methods:
                | jog - Jogs specific robot axis by relative displacement.
                | set_feedrate_override - Sets execution speed override percentage.
    '''

    def jog(self, axis: str, step: float) -> bool:
        '''
            Jogs specific robot axis by relative displacement.

            :param axis: Axis identifier string ('X', 'Y', 'Z', 'Phi', etc.).
            :param step: Relative displacement step value.
            :return: True if command transmitted successfully, False otherwise.
        '''

    def set_feedrate_override(self, pct: int) -> bool:
        '''
            Sets execution speed override percentage.

            :param pct: Speed override percentage between 10 and 200.
            :return: True if command transmitted successfully, False otherwise.
        '''
